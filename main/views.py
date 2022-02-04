import os
import cv2
import time
import glob
import qrcode
import barcode
import numpy as np
from PIL import Image
from datetime import datetime
from pyzbar.pyzbar import decode
from django.shortcuts import render, redirect
from barcode.writer import ImageWriter
from django.utils.encoding import smart_str
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse

set_of_types = [b for b in barcode.PROVIDED_BARCODES] + ['qrcode']\

text_from_camera = ''
type_from_camera = 'TYPE'
text_from_image = ''
type_from_image = 'TYPE'
type_from_generated_image = ''
text_from_generated_image = ''

base_path = 'main/static/images'
uploaded_image = 'uploaded_image.png'
generated_image = 'generated_image.png'
uploaded_image_path = f'{base_path}/{uploaded_image}'
generated_image_path = f'{base_path}/{generated_image}'

# global set_of_types, text_from_camera, type_from_camera, text_from_image, type_from_image, type_from_generated_image, text_from_generated_image, uploaded_image, generated_image, uploaded_image_path, generated_image_path, base_path


def save_uploaded_image(request):
    global uploaded_image_path
    image_current = request.FILES['uploaded_image']
    fs = FileSystemStorage()
    fs.delete(uploaded_image_path)
    fs.save(uploaded_image_path, image_current)


def video_streaming():
    global text_from_camera, type_from_camera
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    media_path = os.path.join(os.getcwd(), "media", "images")
    # create "media/images" folder if doesn't exist
    if not media_path:
        os.mkdir(media_path)

    while True:
        # Capture frame-by-frame
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            # Add text on top of the barcode if there is a barcode in the stream using opencv convert camera frame to numpy array
            color_image = np.asanyarray(frame)

            # decode numpy array to check if there is a barcode in color_image
            # you can add a custom check here to verify if the qr code has right identifier information
            if decode(color_image):
                for brcde in decode(color_image):
                    text_from_camera = brcde.data.decode('utf-8')
                    # if barcode data exists
                    if text_from_camera:
                        type_from_camera = brcde.type
                        # save file as PNG if a QR code is detected
                        today = str(datetime.now().strftime("%d-%m-%y"))
                        image = os.path.join(media_path, f"img_{today}.png")
                        cv2.imwrite(image, frame)

                        pts = np.array([brcde.polygon], np.int32)
                        pts = pts.reshape((-1, 1, 2))

                        # draw polylines on the barcode
                        cv2.polylines(img=color_image, pts=[pts], isClosed=True, color=(0, 255, 0), thickness=3)
                        pts2 = brcde.rect

                        # put text on top of polylines
                        barcode_frame = cv2.putText(img=color_image, text=text_from_camera, org=(pts2[0], pts2[1]),
                                                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.75,
                                                    color=(0, 0, 255), thickness=2)

                        # encode the new barcode_frame that has polylines and barcode data text
                        _, buffer_ = cv2.imencode('.jpg', barcode_frame)

                        # convert barcode_frame to bytes
                        barcode_frame = buffer_.tobytes()

                        # yield output stream with polylines and barcode data text
                        yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + barcode_frame + b'\r\n\r\n'

            # else, yield the normal camera stream
            else:
                frame = buffer.tobytes()
                yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'


def views_detect_from_camera(request):
    global text_from_camera, type_from_camera
    frames = video_streaming()

    if request.is_ajax():
        print('ajax request received')
        time_stamp = str(datetime.now().strftime("%d-%m-%y"))
        image = os.path.join(os.getcwd(), "media", "images", f"img_{time_stamp}.png")
        if os.path.exists(image):
            im = Image.open(image)

            if decode(im):
                for brcde in decode(im):
                    text_from_camera = brcde.data.decode('utf-8')
                    type_from_camera = brcde.type
                    file_saved_at = time.ctime(os.path.getmtime(image))
                    return JsonResponse(data={'text_from_camera': text_from_camera, 'file_saved_at': file_saved_at})
            else:
                return JsonResponse(data={'text_from_camera': None})
        else:
            return JsonResponse(data={'text_from_camera': None})

    else:
        return StreamingHttpResponse(frames, content_type='multipart/x-mixed-replace; boundary=frame')


def views_detect_from_image(request):
    global text_from_image, type_from_image, uploaded_image_path
    save_uploaded_image(request)

    frame = cv2.imread(uploaded_image_path)
    color_image = np.asanyarray(frame)
    detected_barcodes = decode(color_image)
    if detected_barcodes:
        for brcde in detected_barcodes:
            if brcde.data != "":
                text_from_image = brcde.data.decode('utf-8')
                type_from_image = brcde.type
                return redirect(views_main)
    text_from_image = ''
    type_from_image = ''
    return redirect(views_main)


def views_generate_image(request):
    if request.method == 'POST':
        global type_from_generated_image, text_from_generated_image, generated_image_path, base_path

        type_from_generated_image = request.POST['type_from_generated_image']
        text_from_generated_image = request.POST['text_from_generated_image']

        if os.path.isfile(f'{generated_image_path}'):
            os.remove(f'{generated_image_path}')

        if type_from_generated_image == 'qrcode':
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=1)
            qr.add_data(text_from_generated_image)
            qr.make(fit=True)
            imagefile = qr.make_image(fill_color="black", back_color="white")
            imagefile.save(f'{generated_image_path}', options={"write_text": False})
        else:
            try:
                imagefile = barcode.get_barcode(name=type_from_generated_image, code=text_from_generated_image, writer=ImageWriter())
                generated_image_path_custom = f'{generated_image_path}'.replace('.png', '')
                imagefile.save(generated_image_path_custom, options={"write_text": False})
            except:
                return redirect(views_main)

        return redirect(views_main)


def views_main(request):
    global set_of_types, text_from_camera, type_from_camera, text_from_image, type_from_image, type_from_generated_image, text_from_generated_image, uploaded_image, generated_image, uploaded_image_path, generated_image_path
    context = {
        'set_of_types': set_of_types,
        'text_from_camera': text_from_camera, 'type_from_camera': type_from_camera,
        'text_from_image': text_from_image, 'type_from_image': type_from_image,
        'text_from_generated_image': text_from_generated_image, 'type_from_generated_image': type_from_generated_image,
        'generated_image': generated_image,
        'uploaded_image': uploaded_image
    }
    return render(request, 'index.html', context)