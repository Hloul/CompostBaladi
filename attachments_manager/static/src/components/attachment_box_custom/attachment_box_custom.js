/** @odoo-module */

import { AttachmentBox } from '@mail/components/attachment_box/attachment_box';
import AttachmentWebcamDialog from '@attachments_manager/components/attachment_webcam/attachment_webcam';
import AttachmentScreenCastDialog from '@attachments_manager/components/attachment_screencast/attachment_screencast';
import { patch } from 'web.utils';
import Dialog from 'web.Dialog';
const { useState, useRef, onMounted } = owl;
import { useService } from "@web/core/utils/hooks";
import { session } from '@web/session';

Object.assign(AttachmentBox, {
    components: {
        Dialog: Dialog,
        AttachmentWebcamDialog: AttachmentWebcamDialog,
        AttachmentScreenCastDialog: AttachmentScreenCastDialog
    }
});
patch(AttachmentBox.prototype, 'attachments_manager/static/src/components/attachment_box_custom/attachment_box_custom.js', {
    setup() {
        this._super(...arguments);
        this.dialogService = useService("dialog");
        this.action = useService("action");
        this.state = useState({
            hasFavoritesDialog: false,
            hasWebcamDialog: false,
            snapshot: '',
            attachments_favorite: [],
            inputHidden: true,
        });
        this.amThread = this.attachmentBoxView.chatter.thread;
        onMounted(this.mounted);
    },

    toggleInput() {
        this.state.inputHidden = !this.state.inputHidden;
    },

    willUnmount() {
        $(this.el).contextMenu('destroy');
    },

    _openContextMenu(ev) {
        ev.preventDefault();
        $(ev.target).contextMenu();
    },

    _onClickAddAttachment(){
        this.attachmentBoxView.onClickAddAttachment()
    },

    mounted() {
        const self = this;

        $(this.__owl__.refs.root).contextMenu({
            selector: '.oe_button_control_new',
            build: function ($trigger, e) {
                // this callback is executed every time the menu is to be shown
                // its results are destroyed every time the menu is hidden
                // e is the original contextmenu event, containing e.pageX and e.pageY (amongst other data)
                return {
                    callback: function (key, options) {
                        e.target = e.currentTarget;
                        var odoo_callback = self[key].bind(self);
                        odoo_callback(e);
                    },
                    items: {
                        "_onClickAddAttachment": { name: "My device", icon: "fa-folder-open-o", disabled: function () { return false; } },
                        "_onAddURL": {
                            name: "Add URL", icon: "fa-link", disabled: function () {
                                return false;
                            }
                        },
                        "_openFrontCamera": { name: "Camera front", icon: "fa-mobile-phone", disabled: function () { return false; } },
                        "_openRearCamera": { name: "Camera rear", icon: "fa-camera", disabled: function () { return false; } },
                        "_onScreenCast": {
                            name: "From Screen Record", icon: "fa-desktop", disabled: function () {
                                return false;
                            }
                        },
                        "sep4": "---------",
                        "_onGoogleDrivePicker": {
                            name: "From Google Drive", icon: "fa-google-plus", disabled: function () {
                                if ('_onGoogleDrivePicker' in self)
                                    return false;
                                return true;
                            }
                        },
                        "_onMicrosoftOnedrivePicker": {
                            name: "From Microsoft Onedrive", icon: "fa-cloud", disabled: function () {
                                if ('_onMicrosoftOnedrivePicker' in self)
                                    return false;
                                return true;
                            }
                        },
                        "_onDropboxPicker": {
                            name: "From Dropbox", icon: "fa-dropbox", disabled: function () {
                                if ('_onDropboxPicker' in self)
                                    return false;
                                return true;
                            }
                        },
                        // "_onOwnCloudPicker": {name: "From Own Cloud", icon: "fa-soundcloud", disabled: function(){
                        //     if ('_onOwnCloudPicker' in self)
                        //         return false;
                        //     return true;
                        // }},
                        "_onAmazonPicker": {
                            name: "From Amazon", icon: "fa-amazon", disabled: function () {
                                if ('_onAmazonPicker' in self)
                                    return false;
                                return true;
                            }
                        },
                        "_onFacebookPicker": {
                            name: "From Facebook", icon: "fa-facebook", disabled: function () {
                                if ('_onFacebookPicker' in self)
                                    return false;
                                return true;
                            }
                        },
                        "_onInstagramPicker": {
                            name: "From Instagram", icon: "fa-instagram", disabled: function () {
                                if ('_onInstagramPicker' in self)
                                    return false;
                                return true;
                            }
                        },
                        "sep5": "---------",
                        "hide_context": { name: "Close", icon: "fa-remove" }
                    },
                };
            }
        });
    },

    hide_context(ev) {
        ev.stopPropagation();
        ev.preventDefault();
    },

    _hasNoTag(attachment, tag_name) {
        for (let i = 0; i < attachment.tag_ids.length; i++)
            if (attachment.tag_ids[i][1].indexOf(tag_name) + 1)
                return false
        return true
    },

    _onFilterTagThread(ev) {
        if (!ev.target.value) {
            this.attachmentBoxView.chatter.refresh()
            return true
        }

        this.amThread.update({
            originThreadAttachments: [['unlink',
                this.amThread.allAttachments.filter(attachment => this._hasNoTag(attachment, ev.target.value))
            ]],
        });
    },

    _onRefreshThread(ev) {
        ev.stopPropagation();
        ev.preventDefault();
        this.attachmentBoxView.chatter.refresh()
    },

    _onDownloadAll(ev) {
        ev.stopPropagation();
        ev.preventDefault();
        window.location.href = '/web/binary/download_document?res_id=' + this.amThread.id + '&res_model=' + this.amThread.model;
    },

    _openAttachmentManagerPublic(ev) {
        ev.stopPropagation();
        ev.preventDefault();
        const action = {
            type: 'ir.actions.act_window',
            name: this.env._t("Attachment Management public"),
            res_model: 'ir.attachment',
            domain: [['public', '=', true]],
            view_mode: 'tree,form',
            views: [
                [false, 'list'],
                [false, 'form']
            ],
        };
        this.action.doAction(action, {
            onClose: () => this.attachmentBoxView.chatter.refresh()
        })
    },

    _openAttachmentManager(ev) {
        ev.stopPropagation();
        ev.preventDefault();
        const action = {
            type: 'ir.actions.act_window',
            name: this.env._t("Attachment Management current"),
            res_model: 'ir.attachment',
            domain: [
                '&',
                ['res_model', '=', this.amThread.model],
                ['res_id', '=', this.amThread.id]
            ],
            view_mode: 'tree,form',
            views: [
                [false, 'list'],
                [false, 'form']
            ],
        };

        this.action.doAction(action, {
            onClose: () => this.attachmentBoxView.chatter.refresh()
        })

    },

    _openFavoritesManager(ev) {
        ev.stopPropagation();
        ev.preventDefault();
        const action = {
            type: 'ir.actions.act_window',
            name: this.env._t("Attachment Management"),
            res_model: 'ir.attachment',
            domain: [['favorite_users_ids', 'in', session.uid], ['is_favorite', '=', true]],
            view_mode: 'tree,form',
            views: [
                [false, 'list'],
                [false, 'form']
            ],
            params: {
                context: {
                    'default_model_id': this.amThread.model,
                    'default_res_id': this.amThread.id
                }
            }
        };
        this.action.doAction(action, {
            onClose: () => this.attachmentBoxView.chatter.refresh()
        })
    },

    _onAddURL(ev) {
        ev.stopPropagation();
        ev.preventDefault();

        const action = {
            type: 'ir.actions.act_window',
            name: this.env._t("Attachment Management Add URL"),
            res_model: 'ir.attachment.add_url',
            domain: [['favorite_users_ids', 'in', session.uid], ['is_favorite', '=', true]],
            view_mode: 'form,tree',
            target: 'new',
            views: [[false, 'form']],
            context: {
                'default_res_model': this.amThread.model,
                'default_res_id': this.amThread.id
            }
        };
        this.action.doAction(action, {
            onClose: () => this.attachmentBoxView.chatter.refresh()
        })
    },

    _onFavoritesClosed(ev) {
        ev.stopPropagation();
        ev.preventDefault();
        this.state.hasFavoritesDialog = false;
        this.attachmentBoxView.chatter.refresh()
    },

    async _openFavorites(ev) {
        ev.stopPropagation();
        ev.preventDefault();
        const attachmentsFavoritesData = await this.amThread.async(() => this.env.services.rpc({
            model: 'ir.attachment',
            method: 'search_read',
            domain: [['favorite_users_ids', 'in', session.uid], ['is_favorite', '=', true]],
            fields: ['id', 'name', 'mimetype', 'create_uid', 'create_date', 'file_size', 'public', 'type', 'url', 'is_favorite'],
            orderBy: [{ name: 'id', asc: false }],
        }, { shadow: true }));

        this.state.attachments_favorite = await attachmentsFavoritesData.map(data =>
            this.env.models['mail.attachment'].convertData(data)
        ).map(attachment => `mail.attachment_${attachment.id}`);


        this.state.hasFavoritesDialog = true;
    },

    _onScreenCast(ev) {
        this.dialogService.add(AttachmentScreenCastDialog, {
            onCallback: () => {
                try {
                    this.attachmentBoxView.chatter.refresh()
                } catch (e) {
                    console.error('Save to attachments from other side', e)
                }
            },
            res_id: this.amThread.id,
            res_model: this.amThread.model

        });
    },

    _openRearCamera(ev) {
        this.dialogService.add(AttachmentWebcamDialog, {
            mode:true,
            onWebcamCallback: (file) => this.onWebcamCallback(file),
        });
    },

    _openFrontCamera(ev) {
        this.dialogService.add(AttachmentWebcamDialog, {
            mode:false,
            onWebcamCallback: (file) => this.onWebcamCallback(file),
        });
    },

    async onWebcamCallback(file) {
        await this.attachmentBoxView.fileUploader.uploadFiles([file]);
    }

});

export default AttachmentBox;
