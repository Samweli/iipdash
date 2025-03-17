// import * as $ from 'jquery'; // eslint-disable-line no-unused-vars
import * as bootstrap from 'bootstrap';

//
// Enable bootstrap popovers everywhere
//
// document.addEventListener("DOMContentLoaded", function () {
document.addEventListener('DOMContentLoaded', function () {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    // eslint-disable-next-line no-unused-vars
    const popoverList = popoverTriggerList.map((popoverTriggerEl) => {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Layers popovers
    // const layerItemPopoverTemplate = document.querySelector("#layer-item-popover-template").innerHTML
    // document.querySelectorAll(".popover-trigger").forEach((el) => {
    //     let popoverContentId = el.getAttribute("data-popover-content");
    //     let popoverContent = document.querySelector(popoverContentId).innerHTML;
    //     new bootstrap.Popover(el, {
    //         html: true,
    //         content: popoverContent,
    //         placement: 'auto',
    //         template: layerItemPopoverTemplate
    //     });
    // });
});
