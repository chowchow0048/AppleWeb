document.querySelectorAll('.school-button').forEach(button => {
    button.addEventListener('click', function() {
        const alreadyActive = this.classList.contains('active');
        document.querySelectorAll('.school-button').forEach(b => b.classList.remove('active'));
        if (!alreadyActive) {
            this.classList.add('active');
        }

        filterCourses(this.getAttribute('data-school'));
    });
});

const subjectTranslations = {
    physics: '물리',
    chemistry: '화학',
    biology: '생명과학',
    earth_science: '지구과학',
    integrated_science: '통합과학'
};


function filterCourses(school) {
    const day = new Date().toLocaleDateString('ko-KR', { weekday: 'long' }).toLowerCase();
    const url = `/management/api/courses/?day=${day}&school=${school}`;

    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            console.log('MANAGEHOME', data);
            const coursesByGrade = {
                '2학년': { '물리': [], '화학': [], '생명과학': [], '지구과학': [] },
                '1학년': { '통합과학': [] }
            };

            data.forEach(course => {
                const subject = subjectTranslations[course.course_subject];
                if (course.course_grade in coursesByGrade && subject in coursesByGrade[course.course_grade]) {
                    coursesByGrade[course.course_grade][subject].push({
                        id: course.id,
                        time: course.course_time
                    });
                }
            });
            displayCourses(coursesByGrade);
        },
        beforeSend: function() {
            console.log('I am waiting');
        },
        complete: function() {
            console.log('I am done');
        },
        error: function(request, status, error) {
            console.log('I am failed');
            console.error('Error loading the courses:', error);
        }
    });
}

// 원본 코드
// function filterCourses(school) {
//     const url = `/management/api/courses?day=${new Date().toLocaleDateString('ko-KR', { weekday: 'long' }).toLowerCase()}&school=${school}`;

//     // Testing: 일요일 수업
//     // const url = `/management/api/courses?day=일요일&school=${school}`;

//     fetch(url)
//         .then(response => response.json())
//         .then(data => {
//             console.log("MANAGEHOME",data);
//             const coursesByGrade = {
//                 '2학년': { '물리': [], '화학': [], '생명과학': [], '지구과학': [] },
//                 '1학년': { '통합과학': [] }
//             };
        
//             data.forEach(course => {
//                 const subject = subjectTranslations[course.course_subject];
//                 if (course.course_grade in coursesByGrade && subject in coursesByGrade[course.course_grade]) {
//                     coursesByGrade[course.course_grade][subject].push({
//                         id: course.id,
//                         time: course.course_time
//                     });
//                 }
//             });
//             displayCourses(coursesByGrade);
//         })
//         .catch(error => console.error('Error loading the courses:', error));
// }

function displayCourses(coursesByGrade) {
    let allEmpty = true;
    Object.entries(coursesByGrade).forEach(([grade, subjects]) => {
        const container = document.getElementById(`courses-list-gr${grade === '2학년' ? '2' : '1'}`);
        container.innerHTML = '';  // Clear previous content
        const gradeHeader = document.createElement('h2');
        gradeHeader.textContent = `${grade}`;
        gradeHeader.className = 'mt-2 mb-4';
        container.appendChild(gradeHeader);

        let contentFilled = false;
        Object.entries(subjects).forEach(([subject, courses]) => {
            courses.sort((a, b) => (a.time > b.time) ? 1 : ((b.time > a.time) ? -1 : 0));

            if (courses.length > 0) {
                contentFilled = true;
                const subjectContainer = document.createElement('div');
                subjectContainer.className = "d-flex mb-3 align-items-center";
                
                const subjectHeader = document.createElement('h4');
                subjectHeader.textContent = `${subject}`;
                subjectHeader.className = 'nomargin text-start wth-6';

                const buttonsContainer = document.createElement('div');
                buttonsContainer.className = 'course-buttons';

                courses.forEach(course => {
                    const button = document.createElement('button');
                    button.className = 'btn btn-secondary m-2';
                    button.textContent = course.time;
                    button.addEventListener('click', () => redirectToCourse(course.id));
                    buttonsContainer.appendChild(button);
                });

                subjectContainer.appendChild(subjectHeader);
                subjectContainer.appendChild(buttonsContainer);
                container.appendChild(subjectContainer);
            }
        });

        if (!contentFilled) {
            const noCoursesP = document.createElement('p');
            noCoursesP.textContent = '예정된 수업이 없습니다.';
            container.appendChild(noCoursesP);
        } else {
            allEmpty = false;
        }
    });

    if (allEmpty) {
        const mainContainer = document.getElementById('main-courses-container');
        mainContainer.innerHTML = '';  // Clear previous content

        const noCoursesHeader = document.createElement('h2');
        noCoursesHeader.textContent = '수업이 없습니다.';
        mainContainer.appendChild(noCoursesHeader);
    }
}

function redirectToCourse(courseId) {
    window.location.href = `/management/lecture/${courseId}/`;  // 출석부 상세 페이지로 리디렉트
}
