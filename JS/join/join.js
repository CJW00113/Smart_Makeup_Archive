(()=>{
    const $member_id = document.getElementById("member_id");    // 아이디 입력하는 input 박스
    const $check_overlap = document.getElementById("check_overlap");    // 중복인지 확인하는 버튼
    let check_overlap_TF = false;
    const $submitbtbn = document.getElementById('submitbtbn');  // 폼 데이터 전송 버튼

    // 중복 확인 버튼을 눌렀을 경우
    $check_overlap.addEventListener('click', ()=>{
        const jid = $member_id.value;   // input 박스에 입력된 값 가져오기

        if(jid === "") {    // 만약 입력된 내용이 없다면 아래와 같이 실행
            alert("아이디를 입력해 주세요.");
        }
        else {
            // ajax 통신 부분으로 input 박스에 입력된 아이디 값을 컨트롤러에 전송
            fetch(`/join/${jid}`, {
                method : 'POST',
                headers : { "Content-Type" : "application/json" },
                body : JSON.stringify({"member_id" : jid})
            })
            .then((message)=>{ return message.text() })
            .then((message)=>{
                if(message == "exist") {    // 컨트롤러에서 중복인지 아닌지 판단하면서 text를 전송하는데 exist면 중복
                    alert(`${jid}는 중복입니다.`);
                }
                else {
                    $check_overlap.disabled = true;     // 아이디가 중복이 아니므로 버튼 클릭 불가능하게 변경
                    check_overlap_TF = true;
                    $check_overlap.innerText = "사용 가능";     // 중복 체크 버튼은 사용 가능 버튼으로 내용 변경
                }
            });
        }
    });

    // 중복이 체크된 아이디에서 만약 사용자가 아이디를 변경했을 경우
    $member_id.addEventListener('input', ()=>{
        // input 박스의 값을 변경했으므로 다시 버튼을 눌러 중복을 확인해야 하므로 아래와 같이 변경
        $check_overlap.innerText = "중복 확인";     // 다시 중복을 확인하라는 의미에서 중복 확인으로 버튼 내용 변경
        $check_overlap.disabled = false;           // 버튼을 다시 사용할 수 있게 변경
        check_overlap_TF = false;
    });

    $submitbtbn.addEventListener('click', ()=>{
        if(check_overlap_TF == true) {
            document.getElementById('joinform').submit();
        }
        else {
            alert("아이디가 변경되었습니다.");
        }
    });
})();