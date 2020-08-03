class AudioPlaylist extends HTMLElement {
    constructor() {
        super();

        this.curIndex = 0;
    }
   
    connectedCallback() {
        this.list = this.getElementsByTagName('data-list')[0];

        const shadow = this.attachShadow({ mode: 'open' });

        this.audio = document.createElement('audio');
        this.audio.controls = true;
        shadow.appendChild(this.audio);

        this.audio.src = '/tracks/ost/halo';//this.list.children[0].value;
    }
}
customElements.define('audio-playlist', AudioPlaylist);
