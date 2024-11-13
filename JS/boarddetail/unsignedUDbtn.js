(()=>{
    // 모든 삭제 버튼 가져오기
    const deleteButtons = document.querySelectorAll('[id^="CDbtn_"]');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const log = confirm("로그인된 사용자만이 가능한 기능입니다. 로그인 해주세요");
            if(log) {
                window.location.href = `/sign`;
            }
            else {
                window.location.href = `/board`;
            }
        });
    });

    // 모든 수정 버튼 가져오기
    const updateButtons = document.querySelectorAll('[id^="CMbtn_"]');

    updateButtons.forEach(button => {
        button.addEventListener('click', function() {
            const log = confirm("로그인된 사용자만이 가능한 기능입니다. 로그인 해주세요");
            if(log) {
                window.location.href = `/sign`;
            }
            else {
                window.location.href = `/board`;
            }
        });
    });
})();