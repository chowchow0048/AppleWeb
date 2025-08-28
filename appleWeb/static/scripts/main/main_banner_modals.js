document.addEventListener('DOMContentLoaded', () => {
    // 모달 관련 요소들
    const closeBtns = document.querySelectorAll('.close-btn');
    const hideTodayBtns = document.querySelectorAll('.hide-today-btn');
    
    // 쿠키 설정 함수
    const setCookie = (name, value, days) => {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        const expires = `expires=${date.toUTCString()}`;
        document.cookie = `${name}=${value};${expires};path=/`;
    };
    
    // 쿠키 가져오기 함수
    const getCookie = (name) => {
        const cookieName = `${name}=`;
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.indexOf(cookieName) === 0) {
                return cookie.substring(cookieName.length, cookie.length);
            }
        }
        return '';
    };
    
    // 모달 닫기 함수
    const closeModal = (modalId, showNext = false) => {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('show');
            
            // banner1이 닫힐 때 다음 모달 표시
            if (showNext && modalId === 'bannerModal1') {
                setTimeout(() => {
                    showSecondBanner();
                }, 300); // 애니메이션 완료 후 표시
            }
        }
    };
    
    // 모달 열기 함수
    const openModal = (modalId) => {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('show');
        }
    };
    
    // 닫기 버튼 이벤트 리스너
    closeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const modalId = btn.getAttribute('data-modal-id');
            const showNext = modalId === 'bannerModal1';
            closeModal(modalId, showNext);
        });
    });
    
    // 오늘 하루 보지 않기 버튼 이벤트 리스너
    hideTodayBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const modalId = btn.getAttribute('data-modal-id');
            setCookie(modalId, 'hidden', 1); // 하루 동안 쿠키 설정
            const showNext = modalId === 'bannerModal1';
            closeModal(modalId, showNext);
        });
    });
    
    // 화면 크기 확인 함수
    const isMobile = () => {
        return window.innerWidth <= 576;
    };

    // 이미지 존재 여부 확인 함수
    const imageExists = (imageUrl) => {
        return new Promise((resolve) => {
            const img = new Image();
            img.onload = () => resolve(true);
            img.onerror = () => resolve(false);
            img.src = imageUrl;
        });
    };

    // 두 번째 배너 표시 함수 (반응형)
    const showSecondBanner = async () => {
        const secondModalId = isMobile() ? 'bannerModal3' : 'bannerModal2';
        const isHidden = getCookie(secondModalId) === 'hidden';
        
        if (!isHidden) {
            const modal = document.getElementById(secondModalId);
            if (modal) {
                const imgElement = modal.querySelector('img');
                if (imgElement) {
                    const imgSrc = imgElement.getAttribute('src');
                    openModal(secondModalId);
                }
            }
        }
    };

    // 첫 번째 배너만 표시하는 함수
    const showFirstBanner = async () => {
        const modalId = 'bannerModal1';
        const isHidden = getCookie(modalId) === 'hidden';
        
        if (!isHidden) {
            const modal = document.getElementById(modalId);
            if (modal) {
                const imgElement = modal.querySelector('img');
                if (imgElement) {
                    const imgSrc = imgElement.getAttribute('src');
                    openModal(modalId);
                }
            }
        } else {
            // banner1이 숨겨져 있으면 바로 두 번째 배너 표시
            showSecondBanner();
        }
    };
    
    // 페이지 로드 시 첫 번째 배너 모달 표시
    showFirstBanner();
}); 