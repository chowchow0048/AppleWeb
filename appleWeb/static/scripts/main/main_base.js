// Naver map API options
function initMap() {
    // var HOME_PATH = window.HOME_PATH || ',';
    console.log('INIT MAP');
    var mapOptions = {
        center: new naver.maps.LatLng(37.5065445, 127.004894), // 지도의 중심좌표
        zoom: 17, // 지도의 초기 줌 레벨
        minZoom: 15,
        maxZoom: 20,
        zoomControl: true
    };

    var applescience = new naver.maps.Map('map', mapOptions),
    marker = new naver.maps.Marker({
        map: applescience,
        position: mapOptions.center
    });

    var content = [
        '<div class="iw_inner p-3">',
        '   <h3>애플과학</h3> <span class="grey">교습학원, 교습소</span>' ,
        '   <p>서울특별시 서초구 신반포로 189 반포 쇼핑타운 4동 402호<br />',
        '   02-532-1706 |',
        // '       <img src="'+ HOME_PATH +'/img/example/hi-seoul.jpg" width="55" height="55" alt="서울시청" class="thumb" /><br />',
        '       <a href="http://www.apple-science.co.kr" target="_blank">www.apple-science.co.kr</a>',
        '   </p>',
        '</div>'
    ].join('');

    var infowindow = new naver.maps.InfoWindow({
        content: content
    });

    naver.maps.Event.addListener(marker, "click", function(e) {
        if (infowindow.getMap()) {
            infowindow.close();
        } else {
            infowindow.open(applescience, marker);
        }
    });

    infowindow.open(applescience, marker);
}

document.addEventListener('DOMContentLoaded', function() {
    var sessionTime = 90 * 60; 
    // var sessionTime = 10;  // TESTING
    var timerElement = document.getElementById('sessionTimer');

    function updateTimer() {
        var minutes = parseInt(sessionTime / 60, 10);
        var seconds = parseInt(sessionTime % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        timerElement.textContent = minutes + ":" + seconds;

        sessionTime--;

        if (sessionTime < 0) {
            clearInterval(timerInterval);
            alert('세션 만료되었습니다. 다시 로그인 해주세요.');
            window.location = "user/login";
        }
    }

    var timerInterval = setInterval(updateTimer, 1000);
});

window.navermap_authFailure = function () {
    console.log('인증 실패'); // 콘솔에 로그 출력
}

window.onload = () => {
    initMap();
}