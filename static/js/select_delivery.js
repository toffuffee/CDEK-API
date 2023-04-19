let sel = document.getElementById("delivery");

function onChange() {
    var value = sel.value;
    var text = sel.options[sel.selectedIndex].text;

    if(value == "atPoint"){
        document.querySelector('.address-input').value = '';
        document.querySelector('.house-input').value = '';

        document.querySelector('.address').style = "display: none;";
        document.querySelector('.house').style = "display: none;";
        document.querySelector('.postal-code').style = "display: block;";
    }
    if(value == "courier"){
        document.querySelector('.postal-input').value = '';

        document.querySelector('.address').style = "display: block;";
        document.querySelector('.house').style = "display: block;";
        document.querySelector('.postal-code').style = "display: none;";
    }
    console.log(value);
}

sel.onchange = onChange;

 





























// odoo.define('cdek.select_delivery', function (require) {
//     var PublicWidget = require('web.public.widget');
//     var rpc = require('web.rpc');
//     var SelectDelivery = PublicWidget.Widget.extend({
//         selector: '.cdek-form',
//         start: function () {
//             let self = this.el;
//             console.log("lalal");
//         },
//     });
//     PublicWidget.registry.select_delivery = SelectDelivery;
//     return SelectDelivery;
//  });