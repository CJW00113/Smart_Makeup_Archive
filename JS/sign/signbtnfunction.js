(()=>{
    // 로그인 할 때 보이는 버튼
    const $joinbtn = document.getElementById("joinbtn");        // 회원 가입 창으로 이동하는 버튼
    const $findidbtn = document.getElementById("findidbtn");    // 아이디 찾기 기능을 실행하는 버튼
    const $findpwdbtn = document.getElementById("findpwdbtn");      // 비밀번호를 찾기위한 폼을 보여주는 버튼

    // 아이디를 찾을 때 보이는 버튼
    const $escbtn = document.getElementById("escbtn");  // 아이디 찾기 취소 버튼

    // 찾은 아이디를 보여줄 때 보이는 버튼
    const $okbtn = document.getElementById("okbtn");    // 아이디를 찾아서 로그인 화면으로 이동하기 위한 버튼

    // 비밀번호를 찾을 때 보이는 버튼
    const $pwdescbtn = document.getElementById("pwdescbtn");        // 비밀번호 찾을 때 취소 버튼



    // 회원가입 버튼 클릭 시 회원가입 페이지로 이동
    $joinbtn.addEventListener('click', () => {
        window.location.href = '/join';
    });

    // 아이디 찾기 버튼 클릭 시 로그인 폼 숨기고 아이디 찾기 폼 표시
    $findidbtn.addEventListener('click', () => {
        $findid_form.style.display = 'block';
        $login_form.style.display = 'none';
    });

    // 취소 버튼 클릭 시 아이디 찾기 폼 숨기고 로그인 폼 표시
    $escbtn.addEventListener('click', () => {
        $findid_form.style.display = 'none';
        $login_form.style.display = 'block';
    });

    // 아이디 찾고 확인 버튼을 눌렀을 때
    $okbtn.addEventListener('click', ()=>{
        window.location.href = "/sign";
    });

    // 비밀번호 찾을 때 취소 버튼 클릭시
    $pwdescbtn.addEventListener('click', ()=>{
        $login_form.style.display = 'block';    // 로그인 폼 보이게하기
        $findpwd_form.style.display = "none";  // 비밀번호 찾기 폼 안 보이게 하기
    });

    // 비밀번호를 찾는 부분
    $findpwdbtn.addEventListener('click', ()=>{
        $login_form.style.display = 'none';    // 로그인 폼 안보이게 하기
        $findpwd_form.style.display = "block";  // 비밀번호 찾기 폼 보이게 하기
    });
})();