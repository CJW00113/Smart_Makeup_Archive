(()=>{
    const $wbtn = document.getElementById("wbtn");

    $wbtn.addEventListener('click', ()=>{
        const log = confirm("아이디를 로그인해주세요.");    // TF 신호를 주는 메시지 박스 사용해서 로그인 요청
        if(log) {   // 확인을 눌렀으니 로그인 화면으로 이동
            window.location.href="/sign";
        }
        else {      // 취소를 눌렀으니 메인 화면으로 이동
            window.location.href="/index";
        }
    });
})();