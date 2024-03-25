document.addEventListener('DOMContentLoaded', (event) => {
    var timetableModal = document.getElementById('timetableModal');
    timetableModal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget; // 모달을 띄운 요소
        var timetable = button.getAttribute('data-timetable'); // data-timetable 값
        var modalTitle = timetableModal.querySelector('.modal-title');
        var modalBody = timetableModal.querySelector('.modal-body');

        var schoolName = timetable.slice(0, -1); // 마지막 문자를 제외한 나머지 부분
        var grade = timetable.slice(-1); // 마지막 문자
        
        if(timetable == '연합반'){
            modalTitle.textContent = `${schoolName}반 시간표`;    
            
            var imageUrl = "/static/images/세화고1.png";
            modalBody.innerHTML = `<img src="${imageUrl}" class="img-fluid">`; // 이미지 크기 조절
        } else {
            modalTitle.textContent = `${schoolName} ${grade}학년 시간표`;    

            var imageUrl = "/static/images/" + timetable + ".png";
            modalBody.innerHTML = `<img src="${imageUrl}" class="img-fluid">`; // 이미지 크기 조절
        }

        // var imageUrl = "/static/images/" + timetable + ".png";
        // modalBody.innerHTML = `<img src="${imageUrl}" class="img-fluid">`; // 이미지 크기 조절
        // modalBody.innerHTML = `<img src="${imageUrl}" class="img-fluid" style="max-height: 70vh; max-width: 100%;">`; // 이미지 크기 조절
    });
});

