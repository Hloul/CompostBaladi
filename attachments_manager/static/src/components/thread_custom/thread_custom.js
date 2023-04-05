/** @odoo-module */

// import { registerClassPatchModel,registerInstancePatchModel } from '@mail/model/model_core';
import { registerPatch } from '@mail/model/model_core';
import { insertAndReplace } from '@mail/model/model_field_command';

// registerPatch({
//     name: 'mail.thread',
//     recordMethods: {
//         /**
//          * @override
//          */
//         async fetchAttachments() {
//             const attachmentsData = await this.async(() => this.env.services.rpc({
//                 model: 'ir.attachment',
//                 method: 'search_read',
//                 domain: [
//                     ['res_id', '=', this.id],
//                     ['res_model', '=', this.model],
//                 ],
//                 fields: ['id', 'name', 'mimetype', 'create_uid', 'create_date', 'file_size', 'public', 'type', 'url', 'is_favorite', 'website_visible', 'tag_ids'],
//                 orderBy: [{ name: 'id', asc: false }],
//             }, { shadow: true }));
//             this.update({
//                 originThreadAttachments: insertAndReplace(attachmentsData),
//             });
//             this.update({ areAttachmentsLoaded: true });
//         }
//     }
// });
