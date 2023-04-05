/** @odoo-module */

import { Component, xml } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class DocxDialog extends Component { }
DocxDialog.template = xml`
<Dialog title="props.title" size="'large'">
    <t t-if="props.attachment">
        <h1>Filename: <t t-esc="props.attachment.name"/>
        </h1>
        <page>
            <div style="margin: 20px; width: auto;" id="docx">
                <t t-raw="props.html"/>
            </div>
        </page>
        </t>
        <t t-set-slot="buttons">
        <button class="o_AttachmentDeleteConfirmDialog_confirmButton btn btn-primary"
                t-on-click="_onDocxDialogClosed">
        Ok</button>
    </t>
</Dialog>`;
DocxDialog.components = { Dialog };