document.addEventListener('DOMContentLoaded', () => {
    // 모달 관련 요소들
    const bannerModals = document.querySelectorAll('.banner-modal');
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
    const closeModal = (modalId) => {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('show');
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
            closeModal(modalId);
        });
    });
    
    // 오늘 하루 보지 않기 버튼 이벤트 리스너
    hideTodayBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const modalId = btn.getAttribute('data-modal-id');
            setCookie(modalId, 'hidden', 1); // 하루 동안 쿠키 설정
            closeModal(modalId);
        });
    });
    
    // 페이지 로드 시 쿠키 확인하여 모달 표시
    const showBannerModals = () => {
        // 이미지 존재 여부 확인 함수
        const imageExists = (imageUrl) => {
            return new Promise((resolve) => {
                const img = new Image();
                img.onload = () => resolve(true);
                img.onerror = () => resolve(false);
                img.src = imageUrl;
            });
        };

        // 모든 모달 표시 처리
        const processModals = async () => {
            for (const modal of bannerModals) {
                const modalId = modal.id;
                const isHidden = getCookie(modalId) === 'hidden';
                
                if (!isHidden) {
                    // 모달 내 이미지 URL 가져오기
                    const imgElement = modal.querySelector('img');
                    if (imgElement) {
                        const imgSrc = imgElement.getAttribute('src');
                        // 이미지 URL이 실제로 존재하는지 확인
                        try {
                            // /static/images/로 시작하는 경로의 경우 단순하게 존재하는지만 확인 (서버 사이드에서 처리되기 때문)
                            if (imgSrc.includes('/static/images/')) {
                                // 서버 사이드에서 렌더링된 경로라면 모달 표시
                                openModal(modalId);
                            } else {
                                // 외부 URL인 경우 실제 이미지 존재 여부 확인
                                const exists = await imageExists(imgSrc);
                                if (exists) {
                                    openModal(modalId);
                                }
                            }
                        } catch (error) {
                            console.error('이미지 확인 중 오류:', error);
                        }
                    }
                }
            }
        };

        processModals();
    };
    
    // 페이지 로드 시 배너 모달 표시
    showBannerModals();
}); 