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

const dayTranslations = {
    monday: '월요일',
    tuesday: '화요일',
    wednesday: '수요일',
    thursday: '목요일',
    friday: '금요일',
    saturday: '토요일',
    sunday: '일요일'
};

function filterCourses(school) {
    const url = `/management/api/courses/?school=${school}`;

    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            console.log('MANAGE ALLLECTURES', data);
            const coursesByGrade = {};

            data.forEach(course => {
                const grade = course.course_grade;
                const subject = subjectTranslations[course.course_subject] || course.course_subject;
                
                if (!coursesByGrade[grade]) {
                    coursesByGrade[grade] = {};
                }
                if (!coursesByGrade[grade][subject]) {
                    coursesByGrade[grade][subject] = [];
                }
                
                coursesByGrade[grade][subject].push({
                    id: course.id,
                    time: course.course_time,
                    day: dayTranslations[course.course_day] || course.course_day,
                    attendance: course.attendance
                });
            });
            
            displayCourses(coursesByGrade);
        },
        error: function(request, status, error) {
            console.error('Error loading the courses:', error);
        }
    });
}

function displayCourses(coursesByGrade) {
    const container = document.querySelector('.container');
    const coursesContainer = document.getElementById('courses-container');
    if (coursesContainer) {
        coursesContainer.remove();
    }
    
    const newCoursesContainer = document.createElement('div');
    newCoursesContainer.id = 'courses-container';
    container.appendChild(newCoursesContainer);

    if (Object.keys(coursesByGrade).length === 0) {
        const noCoursesHeader = document.createElement('h2');
        noCoursesHeader.textContent = '등록된 수업이 없습니다.';
        newCoursesContainer.appendChild(noCoursesHeader);
        return;
    }

    Object.entries(coursesByGrade).forEach(([grade, subjects]) => {
        const gradeContainer = document.createElement('div');
        gradeContainer.className = 'grade-container mb-5';
        
        const gradeHeader = document.createElement('h2');
        gradeHeader.textContent = `${grade}`;
        gradeHeader.className = 'mt-2 mb-4';
        gradeContainer.appendChild(gradeHeader);

        Object.entries(subjects).forEach(([subject, courses]) => {
            courses.sort((a, b) => {
                if (a.day !== b.day) {
                    return a.day < b.day ? -1 : 1;
                }
                return a.time < b.time ? -1 : 1;
            });

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
                button.textContent = `${course.day} ${course.time}`;
                button.addEventListener('click', () => redirectToCourse(course.id, course.attendance));
                buttonsContainer.appendChild(button);
            });

            subjectContainer.appendChild(subjectHeader);
            subjectContainer.appendChild(buttonsContainer);
            gradeContainer.appendChild(subjectContainer);
        });

        newCoursesContainer.appendChild(gradeContainer);
    });
}

function redirectToCourse(courseId, attendance) {
    if (attendance) {
        localStorage.setItem(`attendance_${courseId}`, JSON.stringify(attendance));
    } else {
        localStorage.removeItem(`attendance_${courseId}`);
    }
    window.location.href = `/management/lecture/${courseId}/`;
}

function loadAttendance(courseId) {
    const attendanceData = localStorage.getItem(`attendance_${courseId}`);
    if (attendanceData) {
        const attendance = JSON.parse(attendanceData);
        const now = new Date();
        const nextClassTime = new Date(attendance.next_class_time);
        
        if (now < nextClassTime) {
            displayAttendance(attendance);
        } else {
            localStorage.removeItem(`attendance_${courseId}`);
        }
    }
}

function displayAttendance(attendance) {
    attendance.students.forEach(student => {
        const checkbox = document.querySelector(`input[name="attendance_${student.id}"]`);
        if (checkbox) {
            checkbox.checked = student.status === 'present';
        }
    });
}

function getCourseIdFromUrl() {
    const path = window.location.pathname;
    const matches = path.match(/\/management\/lecture\/(\d+)\//);
    return matches ? matches[1] : null;
}

document.addEventListener('DOMContentLoaded', (event) => {
    const firstSchoolButton = document.querySelector('.school-button');
    if (firstSchoolButton) {
        firstSchoolButton.click();
    }

    const courseId = getCourseIdFromUrl();
    if (courseId) {
        loadAttendance(courseId);
    }
});