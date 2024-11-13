(()=>{
    const $delbtn = document.querySelectorAll('[id^="imgbtn_"]');
    const deleteArray = new Array();    // 삭제할 이미지를 저장하는 리스트
    const $escbtn = document.getElementById("escbtn");  // 변경 사항을 취소
    const $myForm = document.getElementById("myForm");


    $delbtn.forEach(button => {
        button.addEventListener('click', ()=>{
            const imageId = button.id.split("_")[1];
            
            deleteArray.push(imageId);
            const imgElement = button.previousElementSibling; // 해당 버튼의 이전 형제로 이미지 요소 선택
            
            imgElement.remove(); // 이미지 요소 삭제
            button.remove(); // 삭제 버튼도 제거
        });
    });

    $escbtn.addEventListener('click', ()=>{
        window.history.back();
    });

    $myForm.onsubmit = function() {
        document.getElementById('arrayData').value = JSON.stringify(deleteArray);
    }
})();