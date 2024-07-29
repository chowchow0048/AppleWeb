// timetable modal
document.addEventListener('DOMContentLoaded', (event) => {
    var timetableModal = document.getElementById('timetableModal');
    if (!timetableModal) {
        console.log('Modal element not found');
        return;
    }
    timetableModal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget; // 모달을 띄운 요소
        var timetable = button.getAttribute('data-timetable'); // data-timetable 값
        var modalTitle = timetableModal.querySelector('.modal-title');
        var modalBody = timetableModal.querySelector('.modal-body-custom'); // Ensure this selector is correct
        var schoolName = timetable.slice(0, -1); // 마지막 문자를 제외한 나머지 부분
        var grade = timetable.slice(-1); // 마지막 문자
        console.log('MODAL ONONONONONONONNONONON @!@#!@#!@#!@');
        if (timetable === '1학년') {
            modalTitle.textContent = `1학년 시간표`;
            console.log('1학년');
            var imageUrl = "/static/images/1학년.png";
            modalBody.innerHTML = `<img src="${imageUrl}" class="img-fluid">`;
        } else {
            modalTitle.textContent = `${schoolName} ${grade}학년 시간표`;
            console.log(schoolName);
            var imageUrl = "/static/images/" + timetable + ".png";
            modalBody.innerHTML = `<img src="${imageUrl}" class="img-fluid">`;
        }
    });
});

//test
// document.addEventListener('DOMContentLoaded', function() {
//     // 모든 timetable-box 요소에 대해 이벤트 리스너를 추가
//     document.querySelectorAll('.timetable-box').forEach(box => {
//         box.addEventListener('click', function() {
//             // data-timetable 속성 값을 콘솔에 출력
//             const timetable = this.getAttribute('data-timetable');
//             console.log('Clicked timetable:', timetable);
//         });
//     });
// });

// makeStars: header background module
const makeStars = () => {
    const $sky = document.querySelector(".sky");
    const centerX = window.innerWidth / 2;
    const centerY = window.innerHeight / 2;
    const radius = Math.max(window.innerWidth, window.innerHeight); // 원의 반지름

    const getRandomAngle = () => Math.random() * Math.PI * 2; // 0에서 2π 라디안
    const getRandomRadius = () => Math.sqrt(Math.random()) * radius; // 0에서 반지름까지의 임의의 거리

    const _size = Math.floor(radius); // 별의 개수

    const htmlDummy = new Array(_size).fill().map((_, i) => {
      const angle = getRandomAngle();
      const r = getRandomRadius();
      const x = centerX + r * Math.cos(angle); // 원의 방정식을 사용하여 x 좌표 계산
      const y = centerY + r * Math.sin(angle); // 원의 방정식을 사용하여 y 좌표 계산
      const starRadius = Math.random() * 0.7 + 0.1; // 별의 크기

      return `<circle class='star'
        cx=${x}
        cy=${y}
        r=${starRadius}
        className="star" />`
    }).join('');
    
    $sky.innerHTML = htmlDummy;
}

// AJAX 처리: 로그인
// document.addEventListener('DOMContentLoaded', function() {
//     const loginForm = document.getElementById('loginForm');
//     loginForm.addEventListener('submit', function(e) {
//         e.preventDefault();
//         const formData = new FormData(loginForm);
//         fetch('/path/to/login/', {
//             method: 'POST',
//             body: formData
//         }).then(response => response.json())
//           .then(data => {
//               if (data.success) {
//                   $('#loginModal').modal('hide');
//                   console.log('로그인 성공');
//               } else {
//                   console.log('로그인 실패');
//               }
//           }).catch(error => console.error('Error:', error));
//     });
// });

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
        '       <a href="https://www.banpo-applecom" target="_blank">www.banpo-apple.com</a>',
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

window.navermap_authFailure = function () {
    console.log('인증 실패'); // 콘솔에 로그 출력
}

// CALL FUNCTIONS
window.onresize = () => {
    makeStars();
}

window.onload = () => {
    makeStars();
    initMap();
}