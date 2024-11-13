(()=>{
    const $email = document.getElementById("email");    // 이메일
    const $phone = document.getElementById("phone");    // 전화번호
    const $sbbtn = document.getElementById("sbbtn");    // 아이디 찾기 버튼
    const $member_id = document.getElementById("member_id");        // 아이디 출력하기 위한 label

    // 이메일과 전화번호로 아이디 찾기
    $sbbtn.addEventListener('click', ()=>{
        const $emailvalue = $email.value;
        const $phonevalue = $phone.value;

        if($emailvalue == "") {
            alert("이메일을 작성해주세요");
            return;
        }
        if($phonevalue == "") {
            alert("전화번호을 작성해주세요");
            return;
        }
        if($phonevalue != "" && $emailvalue != "") {
            fetch(`/searchId`, {
                method : 'POST',
                headers : { "Content-Type" : "application/json" },
                body : JSON.stringify({"email" : $emailvalue, "phone" : $phonevalue})
            })
            .then((message) => { return message.text()})
            .then((message) => {
                if(message == "fails") {
                    alert(`${$emailvalue}로 아이디를 찾을 수 없습니다.`);
                }
                else {
                    $findid_form.style.display = 'none';
                    $printid_form.style.display = "block";
                    $member_id.value = message;
                }
            })
            .catch((Error) => {
                console.error('Error:', Error); // 에러 처리
            });
        }
    });
})();