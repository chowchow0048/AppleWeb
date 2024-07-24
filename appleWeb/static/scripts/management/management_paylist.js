document.addEventListener("DOMContentLoaded", function() {
    const selectAllButton = document.getElementById("selectAllPayments");
    const processPaymentsButton = document.getElementById("processPayments");
    const paymentCheckboxes = document.querySelectorAll(".payment-checkbox");

    selectAllButton.addEventListener("click", function() {
        const allChecked = Array.from(paymentCheckboxes).every(checkbox => checkbox.checked);
        paymentCheckboxes.forEach(checkbox => {
            checkbox.checked = !allChecked;
            // console.log(checkbox);
        });
    });

    processPaymentsButton.addEventListener("click", function() {
        const selectedUsers = Array.from(paymentCheckboxes)
                                   .filter(checkbox => checkbox.checked)
                                   .map(checkbox => ({
                                       id: checkbox.getAttribute("data-user-id"),
                                       school: checkbox.closest("tr").querySelector("td:nth-child(1)").textContent,
                                       grade: checkbox.closest("tr").querySelector("td:nth-child(2)").textContent,
                                       name: checkbox.closest("tr").querySelector("td:nth-child(3)").textContent,
                                   }));

        if (selectedUsers.length > 0) {
            const userDetails = selectedUsers.map(user => `${user.school} ${user.grade} ${user.name}`).join("\n");
            const message = `${selectedUsers.length}명의 결제를 진행하시겠습니까?\n\n결제 학생 목록:\n${userDetails}`;

            if (confirm(message)) {
                selectedUsers.forEach(user => {
                    processPayment(user.id);
                });
            }
        } else {
            alert("결제 확인할 학생을 선택하세요.");
        }
    });

    function processPayment(userId) {
        fetch(`/management/confirm-payment/${userId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            },
        })
        .then(response => response.json())
        .then(data => {
            // alert(data.message);
            location.reload();
        })
        .catch(error => console.error('Error:', error));
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
