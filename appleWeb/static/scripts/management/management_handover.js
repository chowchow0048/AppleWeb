// 검색기능 보류
// document.getElementById('handover-search').addEventListener('input', function() {
//     const query = this.value.toLowerCase();

//     // AJAX 요청
//     fetch(`/management/handover/search/?query=${query}`)
//         .then(response => {
//             console.log(response);  // 응답 객체 확인
//             return response.json(); // 응답을 JSON으로 파싱
//         })
//         .then(data => {
//             console.log(data);  // JSON 데이터 확인
//             const tableBody = document.getElementById('handover-tbody');
//             tableBody.innerHTML = '';  // 기존 데이터를 초기화

//             if (data.results && data.results.length > 0) {  // data.results가 undefined가 아닌지 확인
//                 data.results.forEach(handover => {
//                     const row = document.createElement('tr');
//                     row.innerHTML = `
//                         <td>${handover.created_date} ${handover.shift} 행정</td>
//                         <td>${handover.author}</td>
//                         <td>${handover.created_date}</td>
//                     `;
//                     row.onclick = () => {
//                         window.location.href = `/management/handover/${handover.id}`;
//                     };
//                     tableBody.appendChild(row);
//                 });
//             } else {
//                 tableBody.innerHTML = '<tr><td colspan="3">인수인계가 없습니다.</td></tr>';
//             }
//         })
//         .catch(error => console.error('Error fetching handovers:', error));
// });
