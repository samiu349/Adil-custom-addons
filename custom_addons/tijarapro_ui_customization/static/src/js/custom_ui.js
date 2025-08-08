/** @odoo-module **/

import {WebClient} from "@web/webclient/webclient";
import {patch} from "@web/core/utils/patch";

// ✅ Changer le titre
patch(WebClient.prototype, {
    setup() {
        super.setup();
        this.title.setParts({zopenerp: "TIJARAPRO"});

        // Observe et applique après navigation
        setInterval(customizeUI, 10);
    }
});

// ✅ Fonction pour modifier le DOM à chaque changement de route
function customizeUI() {
    // Bouton Enregistrer
    document.querySelectorAll('button.o_form_button_save').forEach(btn => {
        const icon = btn.querySelector('i.fa');
        if (icon && !btn.textContent.includes("Enregistrer")) {
            const label = document.createElement('span');
            label.textContent = " Enregistrer";
            icon.after(label);
        }
    });
    // Bouton Cancel
    document.querySelectorAll('button.o_form_button_cancel').forEach(btn => {
        const icon = btn.querySelector('i.fa');
        if (icon && !btn.textContent.includes("Annuler")) {
            const label = document.createElement('span');
            label.textContent = " Annuler";
            icon.after(label);
        }
    });
    // Bouton Action
    document.querySelectorAll('.o-dropdown.dropdown button i.fa-cog').forEach(icon => {
        const parent = icon.parentElement;
        if (parent && !parent.innerText.includes("Actions")) {
            icon.insertAdjacentText("afterend", " Actions");
        }
    });

    // Supprimer "Mon compte Odoo.com"


    // ✅ Supprimer les entrées "Documentation", "Assistance", "Raccourcis"
    document.querySelectorAll('.dropdown-item').forEach(item => {
        const text = item.textContent?.trim();
        if (["Documentation", "Assistance", "Mon compte Odoo.com"].includes(text)) {
            item.remove();
        }
    });

    // Modifier "Odoo - Nouveau"
    document.querySelectorAll("span").forEach(el => {
        if (el.textContent.includes("Odoo - Nouveau")) {
            el.textContent = "TIJARA-PRO";
            const img = el.previousElementSibling;
            if (img && img.tagName === "IMG") {
                img.setAttribute("src", "/tijarapro_ui_customization/static/src/img/tijarapro_logo.png");
            }
        }
    });

    // ✅ Afficher le nom de l'utilisateur
    const isDebug = window.location.search.includes('debug=1');
    if (!isDebug) {
        document.querySelectorAll(".o_user_menu .oe_topbar_name.d-none").forEach(el => {
            el.classList.remove("d-none");
        });
        document.querySelectorAll(".o_user_menu mark.d-block").forEach(el => {
            el.classList.add("d-none");
        });
    }


    // ✅ Remplacer l'icône "fa-comments" par "fa-envelope"
    document.querySelectorAll('i.fa.fa-lg.fa-comments').forEach(icon => {
        icon.classList.remove('fa-comments');
        icon.classList.add('fa-envelope');
    });


    // Remplacer la classe btn-secondary par btn-outline-info
    document.querySelectorAll('button.o_switch_view').forEach(btn => {

        if (btn.classList.contains('btn-secondary')) {
            btn.classList.remove('btn-secondary');
            btn.classList.add('btn-outline-info');
        }
    });
    // Modifier l'attribut data-tooltip
    document.querySelectorAll('button.o_switch_view.o_list').forEach(btn => {
        btn.setAttribute('data-tooltip', 'Vue Liste');
    });
    document.querySelectorAll('button.o_switch_view.o_kanban').forEach(btn => {
        btn.setAttribute('data-tooltip', 'Vue Kanban');
    });
    document.querySelectorAll('button.o_switch_view.o_calendar').forEach(btn => {
        btn.setAttribute('data-tooltip', 'Vue Calandrier');
    });
    document.querySelectorAll('button.o_switch_view.o_pivot').forEach(btn => {
        btn.setAttribute('data-tooltip', 'Tableau croisé dynamique');
    });
    document.querySelectorAll('button.o_switch_view.o_graph').forEach(btn => {
        btn.setAttribute('data-tooltip', 'Vue Graphique');
    });
    document.querySelectorAll('button.o_switch_view.o_activity').forEach(btn => {
        btn.setAttribute('data-tooltip', 'Activités');
    });


    document.querySelectorAll('.o_view_nocontent').forEach(div => {
        // Appliquer un fond blanc
        div.style.background = 'white';

        // ✅ Remplacer le background-image du ::before de .o_view_nocontent_smiling_face
        const styleId = 'tijarapro-nocontent-smiling-face-style';
        if (!document.getElementById(styleId)) {
            const style = document.createElement('style');
            style.id = styleId;
            style.innerHTML = `
        .o_view_nocontent .o_nocontent_help .o_view_nocontent_smiling_face::before {
            background: transparent url(/web/image/res.company/1/favicon) no-repeat center !important;
            background-size: contain !important;
        } `;
            document.head.appendChild(style);
        }

    });


    document.querySelectorAll('.mk_apps_sidebar_name').forEach(div => {
        div.style.fontSize = '14px';
        div.style.fontWeight = 'bold';
    });


    document.querySelectorAll('.o_menu_sections').forEach(div => {
        div.style.fontSize = '0.7rem';
    });

    document.querySelectorAll('.o_menu_sections .dropdown-menu').forEach(menu => {
        menu.style.fontSize = '0.7rem';
    });


}

