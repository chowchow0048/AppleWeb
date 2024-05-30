document.addEventListener('DOMContentLoaded', event => {
    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
            document.body.classList.toggle('sb-sidenav-toggled');
        }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            // console.log('CLICKED@@@@@@@');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        })
    }

});


document.addEventListener('DOMContentLoaded', function() {
    var sessionTime = 90 * 60;  // 90분을 초로 환산
    var timerElement = document.getElementById('sessionTimer');

    function updateTimer() {
        var minutes = parseInt(sessionTime / 60, 10);
        var seconds = parseInt(sessionTime % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        timerElement.textContent = minutes + ":" + seconds;

        // 시간 감소
        sessionTime--;

        // 시간이 0 이하면 타이머를 멈추고 세션 만료 처리
        if (sessionTime < 0) {
            clearInterval(timerInterval);
            alert('세션 만료되었습니다. 다시 로그인 해주세요.');
            window.location = "{% url 'user_login' %}"; // 로그인 페이지로 리다이렉션
        }
    }

    var timerInterval = setInterval(updateTimer, 1000);
});