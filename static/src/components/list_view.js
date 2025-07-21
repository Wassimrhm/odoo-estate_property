/* @odoo-module */
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class ListViewAction extends Component {
    static template = "estate_module.ListView";
}

registry.category("actions").add("estate_module.list_view_action", ListViewAction);

