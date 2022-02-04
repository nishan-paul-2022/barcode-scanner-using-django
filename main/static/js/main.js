    function customized_select() {
        /*look for any elements with the class "id07":*/
        let x = document.getElementsByClassName("id07");
        let l = x.length;

        for (let i = 0; i < l; i++) {
            let selElmnt = x[i].getElementsByTagName("select")[0];
            let ll = selElmnt.length;

            /*for each element, create a new DIV that will act as the selected item:*/
            let a = document.createElement("DIV");
            a.setAttribute("class", "id08");
            a.innerHTML = selElmnt.options[selElmnt.selectedIndex].innerHTML;
            x[i].appendChild(a);

            /*for each element, create a new DIV that will contain the option list:*/
            let b = document.createElement("DIV");
            b.setAttribute("class", "id10 id11");

            for (let j = 1; j < ll; j++) {
                /*for each option in the original select element, create a new DIV that will act as an option item:*/
                let c = document.createElement("DIV");
                c.innerHTML = selElmnt.options[j].innerHTML;
                c.addEventListener("click", function(e) {
                    /*when an item is clicked, update the original select box, and the selected item:*/
                    let s = this.parentNode.parentNode.getElementsByTagName("select")[0];
                    let sl = s.length;
                    let h = this.parentNode.previousSibling;

                    for (let m = 0; m < sl; m++) {
                        if (s.options[m].innerHTML === this.innerHTML) {
                            s.selectedIndex = m;
                            h.innerHTML = this.innerHTML;
                            let y = this.parentNode.getElementsByClassName("id12");
                            let yl = y.length;
                            for (let k = 0; k < yl; k++) {
                                y[k].removeAttribute("class");
                            }
                            this.setAttribute("class", "id12");
                            break;
                        }
                    }

                    h.click();
                });
                b.appendChild(c);
            }

            x[i].appendChild(b);

            a.addEventListener("click", function(e) {
                /*when the select box is clicked, close any other select boxes, and open/close the current select box:*/
                e.stopPropagation();
                close_select_option(this);
                this.nextSibling.classList.toggle("id11");
                this.classList.toggle("id09");
            });
        }


        function close_select_option(elmnt) {
            /*a function that will close all select boxes in the document, except the current select box:*/
            let arrNo = [];
            let x = document.getElementsByClassName("id10");
            let y = document.getElementsByClassName("id08");
            let xl = x.length;
            let yl = y.length;

            for (let i = 0; i < yl; i++) {
                if (elmnt === y[i])
                  arrNo.push(i)
                else
                  y[i].classList.remove("id09");
            }

            for (let i = 0; i < xl; i++) {
                if (arrNo.indexOf(i))
                    x[i].classList.add("id11");
            }
        }

        /*if the user clicks anywhere outside the select box, then close all select boxes:*/
        document.addEventListener("click", close_select_option);
    }


    function get_image_preview(input) {
        if (input.files && input.files[0]) {
            let reader = new FileReader();
            reader.onload = function (e) {
                $('#id18').attr('src', e.target.result);
                $('#id18').css('width','50%');
                $('#id18').css('height','auto');
            };
            reader.readAsDataURL(input.files[0]);
        }
    }

    customized_select();