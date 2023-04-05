/** @odoo-module */

import { session } from '@web/session';
import { registerPatch } from '@mail/model/model_core';

registerPatch({
  name: 'FileUploader',
  recordMethods: {
        /**
     * @override
    */
         async uploadFiles(files) {
          if (session.am_compress_jpeg){
              let compress_files = [...files];
              for (let i = 0; i < compress_files.length; i++)
                  if (compress_files[i].type === 'image/jpeg' ||
                      compress_files[i].type === 'image/png' ||
                      compress_files[i].type === 'image/webp')
                      compress_files[i] = await this.compress(compress_files[i]);
              files = compress_files;
          }
          // TODO super
          await this._performUpload({ files });
          if (!this.exists()) {
              return;
          }
          if (this.fileInput && this.fileInput.el) {
              this.fileInput.el.value = '';
          }
          if (this.chatterOwner && !this.chatterOwner.attachmentBoxView) {
              this.chatterOwner.openAttachmentBoxView();
          }
          this.messaging.messagingBus.trigger('o-file-uploader-upload', { files });


        //   await this._performUpload({
        //     composer: this.composerView && this.composerView.composer,
        //     files,
        //     thread: this.thread,
        // });
        // this._fileInputRef.el.value = '';
      },
  
      async compress(file) {
        let def = $.Deferred();
        //const width = 500;
        //const height = 300;
        const quality = session.am_compress_jpeg_quality;
        const fileName = file.name;
        const fileType = file.type;
        const reader = new FileReader();
  
        reader.readAsDataURL(file);
        reader.onload = event => {
          const img = new Image();
  
          img.src = event.target.result;
          img.onload = () => {
            const elem = document.createElement('canvas');
            //elem.width = img.width;
            //elem.height = img.height;
            elem.width = img.naturalWidth;
            elem.height = img.naturalHeight;
            
            const ctx = elem.getContext('2d');
            // img.width и img.height будет содержать оригинальные размеры
            //ctx.drawImage(img, 0, 0, img.width, img.height);
            ctx.drawImage(img, 0, 0);
            ctx.canvas.toBlob((blob) => {
              const file = new File([blob], fileName, {
                type: fileType,
                lastModified: Date.now()
              });
              def.resolve(file);
  
            }, fileType, parseFloat(quality));
          };
          reader.onerror = error => console.log(error);
        };
        return def;
      }
  }
})
// patch(FileUploader.prototype, 'attachments_manager/static/src/models/file_uploader_custom.js', {

// });  

