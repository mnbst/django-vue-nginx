const loc = window.location;
let wsStart = "ws://";
if (loc.protocol === "https:") {
    wsStart = "wss://";
}
export const getVideoList = wsStart + loc.host + loc.pathname + "get_video_list";
export const getCaption = wsStart + loc.host + loc.pathname + "get_caption";