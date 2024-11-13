(()=>{
    const $editbtn = document.getElementById("editbtn");        // 수정 버튼
    const $deletebtn = document.getElementById("deletebtn");    // 삭제 버튼

    $editbtn.addEventListener('click', ()=>{
        const log = confirm("로그인된 사용자만이 사용가능한 기능입니다. 로그인 화면으로 이동하겠습니까?");
        if(log) {
            window.location.href = `/sign`;
        }
        else {
            window.location.href = `/board`;
        }
    });
    $deletebtn.addEventListener('click', ()=>{
        const log = confirm("로그인된 사용자만이 사용가능한 기능입니다. 로그인 화면으로 이동하겠습니까?");
        if(log) {
            window.location.href = `/sign`;
        }
        else {
            window.location.href = `/board`;
        }
    });
})();