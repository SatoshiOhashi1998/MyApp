
document.addEventListener('DOMContentLoaded', function() {
    init();
    setupEventListeners();
    updateRecommendVideo();
});

function init() {
    document.title = "動画鑑賞";
    basePath = "C:/Users/user/PycharmProjects/MyUtilProject/MyApp/FlaskApp/app/"
    nowUseDir = "static/video/asmr/";
    mainVideo = document.querySelector("#mainVideo");
    randomOrder = document.querySelector("#randomOrder");
    loopOrder = document.querySelector("#loopOrder");
    playedVideos = [];
}

function setupEventListeners() {
    $("h3").click(updateRecommendVideo);

    $("#selectDir").change(function() {
        var useDir = $(this).val();
        nowUseDir = useDir;
        fetchAndLoadVideos(useDir);
    });

    $("#selectVideo").change(function() {
        var video = $(this).val();
        updateMainVideo(nowUseDir + video, video);
    });

    $("#mainVideo").on("ended", handleVideoEnd);

    document.addEventListener('keydown', handleKeydown);

    $('.form-select').select2();
}

function handleVideoEnd() {
    var videoPaths = document.querySelectorAll(".videoPathContainer");
    if (randomOrder.checked) {
        playRandomVideo(videoPaths);
    } else if (loopOrder.checked) {
        mainVideo.play();
    } else {
        playNextVideo(videoPaths);
    }
}

function handleKeydown(event) {
    const skipAmount = 10; // キーの移動量（秒）
    if (event.key === 'ArrowLeft') {
        mainVideo.currentTime -= skipAmount;
    } else if (event.key === 'ArrowRight') {
        mainVideo.currentTime += skipAmount;
    }
}

function getRandam(n, m) {
    return Math.floor(Math.random() * (m + 1 - n)) + n;
}

function setVideoTime(t) {
    mainVideo.currentTime = t;
}

function updateUrlWithParams(dir, video) {
    const currentUrl = new URL(window.location.href);
    currentUrl.searchParams.set('v', video);
    currentUrl.searchParams.set('dir', dir);
    window.history.pushState({}, '', currentUrl);
}

function updateMainVideo(src, title, usedir=nowUseDir) {
    mainVideo.src = src;
    document.title = title;
    updateUrlWithParams(usedir, title);
    $("#selectVideo").val(title);
    $("#selectVideo").next().find("#select2-selectVideo-container").html(title);
    $("#selectDir").val(usedir);
    $("#selectDir").next().find("#select2-selectDir-container").html(usedir);
}

function playRandomVideo(videoPaths) {
    var availableVideos = Array.from(videoPaths).filter(function(videoPath) {
        return !playedVideos.includes(videoPath.value);
    });

    var index = getRandam(0, availableVideos.length - 1);
    var selectedVideo = availableVideos[index];
    updateMainVideo(nowUseDir + selectedVideo.value, selectedVideo.value);
    playedVideos.push(selectedVideo.value);
}

function playNextVideo(videoPaths) {
    var beforeWatchVideo = $("#selectVideo").val();
    var selectedVideoIndex = videoPaths.findIndex(videoPath => videoPath.value === beforeWatchVideo);

    if (selectedVideoIndex != -1 && selectedVideoIndex < videoPaths.length - 1) {
        var nextVideo = videoPaths[selectedVideoIndex + 1];
        updateMainVideo(nowUseDir + nextVideo.value, nextVideo.value);
    }
}

function fetchAndLoadVideos(useDir) {
    $.ajax({
        data: { use_dir: basePath + useDir },
        type: 'POST',
        url: '/watchVideo'
    })
    .done(function(data) {
        $("#selectVideo").empty();
        data.response.forEach(videoPath => {
            var template = `<option value='${videoPath}' class='videoPathContainer'>${videoPath}</option>`;
            $("#selectVideo").append(template);
        });

        // 最初の動画をメインビデオで再生
        updateMainVideo(nowUseDir + data.response[0], data.response[0]);
        updateRecommendVideo();
    });
}

function getThumbnailPath(videoTitle) {
    return `static/image/videoThumbnail/${videoTitle.replace('.mp4', '.jpg')}`;
}

function updateRecommendVideo() {
    var allVideoPaths = Array.from(document.querySelectorAll(".videoPathContainer"));
    var randomVideoPaths = [];

    while (randomVideoPaths.length < 3) {
        var randomIndex = Math.floor(Math.random() * allVideoPaths.length);
        var randomPath = allVideoPaths.splice(randomIndex, 1)[0];
        randomVideoPaths.push(randomPath.value);
    }

    $(".recommendations-list").empty();
    randomVideoPaths.forEach(videoPath => {
        var escapedVideoPath = videoPath.replace(/'/g, "\\'");
        var videoSrc = nowUseDir + escapedVideoPath;
        var thumbnailSrc = getThumbnailPath(escapedVideoPath);

        var videoItem = `
            <li>
                <div class="video-item">
                    <img src="${thumbnailSrc}" alt="${escapedVideoPath}" class="video-thumbnail" 
                         onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
                    <video src="${videoSrc}" style="display: none;" 
                           onerror="this.style.display='block'; this.previousElementSibling.style.display='none';"></video>
                    <div class="video-description">${escapedVideoPath}</div>
                </div>
            </li>`;
        $(".recommendations-list").append(videoItem);
    });

    $(".recommendations-list li").click(function() {
        var videoPath = $(this).find("video").attr("src");
        var videoTitle = $(this).find(".video-description").text();
        updateMainVideo(videoPath, videoTitle);
    });
}
