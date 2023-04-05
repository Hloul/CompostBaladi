/** @odoo-module */

const { useState, useRef, Component } = owl;
import { session } from '@web/session';
import { useService } from "@web/core/utils/hooks";

class AttachmentScreenCastDialog extends Component {
    param_init (){
        this.dataChunks = [];
        this.mediaRecorder = null;
        this.videoBlob = null;
    }

    async setup() {
        super.setup();
        this.rpc = useService("rpc");
        this.state = useState({
            recording: null,
            screenStream: null,
            voiceStream: null,
        });
        this.param_init()
        this.videoRef = useRef('videoRef');
        this.linkRef = useRef('linkRef');
        if (!this.state.screenStream && !this.state.voiceStream) {
            // параллельное ожидание запроса на доступы
            // await Promise.all([this.startVideo(), this.startAudio()]);
            await this.startVideo()
            await this.startAudio()
        }
    }

    getBody() {
        return _.str.sprintf(
            this.env._t(`You can record video screen or voice microphone`),
        );
    }

    getTitle() {
        return this.env._t("Attachments manager Screen Recording");
    }

    async startVideo() {
        if (navigator.mediaDevices.getDisplayMedia) {
            try {
                const _screenStream = await navigator.mediaDevices.getDisplayMedia({
                    video: true
                })
                this.state.screenStream = _screenStream
            } catch (e) {
                console.error('*** getDisplayMedia', e)
            }
        } else {
            console.warn('*** getDisplayMedia not supported')
        }
    }

    async startAudio() {
        if (navigator.mediaDevices.getUserMedia) {
            if (this.state.screenStream) {
                try {
                    const _voiceStream = await navigator.mediaDevices.getUserMedia({
                        audio: true
                    })
                    this.state.voiceStream = _voiceStream
                } catch (e) {
                    console.error('*** getUserMedia', e)
                    this.state.voiceStream = 'unavailable';
                } finally {
                }
            }
            else
                console.warn('*** screenStream is null')
        } else {
            console.warn('*** getUserMedia not supported')
        }
    }

    startStopButton(ev) {
        if (!this.state.recording) {
            this.startRecording()
        } else {
            if (this.mediaRecorder) {
                this.mediaRecorder.stop()
                this.stopRecording()
            }
        }
    }

    _onClickCancel() {
        this.param_init();
        if (this.state.screenStream){
            const tracks = this.state.screenStream.getVideoTracks()
            if (tracks) {
                // get video track to call stop on it
                if (tracks && tracks[0] && tracks[0].stop) tracks[0].stop();
            }
        }
        if (this.state.voiceStream){
            const tracksA = this.state.voiceStream.getAudioTracks()
            if (tracksA) {
                // get video track to call stop on it
                if (tracksA && tracksA[0] && tracksA[0].stop) tracksA[0].stop();
            }
        }
        this.props.close();
    }
    blobToBase64 (blob) {
        const reader = new FileReader();
        reader.readAsDataURL(blob);
        return new Promise(resolve => {
          reader.onloadend = () => {
            resolve(reader.result);
          };
        });
    }
    async saveButton() {
        const today = new Date();
        const dateTimeStr = today.toISOString().substring(0, 19).replaceAll(":","-")
        // const file = await new File([this.videoBlob], `${dateTimeStr}-${session.partner_display_name}.webm`);
        // await this.props.onCallback(file);
        const base64 = await this.blobToBase64(this.videoBlob)
        await this.rpc("/web/dataset/call_kw", {
            model: "ir.attachment",
            method: "create",
            kwargs: {
            },
            args: [{
                name: `${dateTimeStr}-${session.partner_display_name}.webm`,
                res_model: this.props.res_model,
                res_id: this.props.res_id,
                datas: base64.split(',')[1],
            }],
        });
        this.props.onCallback()
        this._onClickCancel();
    }

    stopRecording() {
        const today = new Date();
        const dateTimeStr = today.toISOString().substring(0, 19).replaceAll(":","-")
        this.state.recording = false;

        this.videoBlob = new Blob(this.dataChunks, {
            type: 'video/webm'
        })

        const videoSrc = URL.createObjectURL(this.videoBlob)

        this.videoRef.el.src = videoSrc
        this.linkRef.el.href = videoSrc
        this.linkRef.el.download = `${dateTimeStr}-${session.partner_display_name}.webm`

        this.mediaRecorder = null
        this.dataChunks = []
    }

    async startRecording() {
        if (this.state.screenStream && this.state.voiceStream && !this.mediaRecorder) {
            this.state.recording = true;

            this.videoRef.el.removeAttribute('src')
            this.linkRef.el.removeAttribute('href')
            this.linkRef.el.removeAttribute('download')

            let mediaStream
            if (this.state.voiceStream === 'unavailable') {
                mediaStream = this.state.screenStream
            } else {
                mediaStream = new MediaStream([
                    ...this.state.screenStream.getVideoTracks(),
                    ...this.state.voiceStream.getAudioTracks()
                ])
            }

            this.mediaRecorder = new MediaRecorder(mediaStream)
            this.mediaRecorder.ondataavailable = ({ data }) => {
                this.dataChunks.push(data)
            }
            this.mediaRecorder.start(250)
        }

    }

}
AttachmentScreenCastDialog.props = {
    onCallback: { type: Function, optional: true },
    close: Function,
    res_id: { type: Number, optional: true },
    res_model: { type: String, optional: true },
};

AttachmentScreenCastDialog.defaultProps = {
    onCallback: () => { },
};

AttachmentScreenCastDialog.template = 'attachments_manager.AttachmentScreenCastDialog'
export default AttachmentScreenCastDialog;