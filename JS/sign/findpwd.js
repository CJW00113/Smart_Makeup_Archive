(()=>{
    const $pwdmember_id = document.getElementById("pwdmember_id");  // 비밀번호 찾을 때 아이디
    const $pwdemail = document.getElementById("pwdemail");          // 비밀번호 찾을 때 이메일
    const $member_pwd = document.getElementById("member_pwd");          // 새 비밀번호
    const $checkmember_pwd = document.getElementById("checkmember_pwd");    // 새 비밀번호 확인
    const $pwdfindokbtn = document.getElementById("pwdfindokbtn");      // 비밀번호를 확인했고 로그인 페이지로 넘어가기 위한 확인 버튼
    const $pwdokbtn = document.getElementById("pwdokbtn");          // 비밀번호 찾을 때 확인 버튼

    let pwdid;
    // 비밀번호 찾을 때 이메일 아이디 입력 후 확인 버튼 클릭할 때
    $pwdokbtn.addEventListener('click', ()=>{
        pwdid = $pwdmember_id.value;
        const pwdemail = $pwdemail.value;

        if (pwdid == "") {
            alert("아이디를 입력해주세요");
            return;
        }
        if (pwdemail == "") {
            alert("이메일을 입력해주세요");
            return;
        }
        if (pwdid != "" && pwdemail != "") {
            fetch(`/searchpwd`, {
                method : 'POST',
                headers : { "Content-Type" : "application/json" },
                body : JSON.stringify({"member_id" : pwdid, "email" : pwdemail})
            })
            .then((message) => { return message.text()})
            .then((message) => {
                if(message == "fails") {
                    alert(`${pwdid}로 비밀번호를 찾을 수 없습니다.`);
                }
                else {
                    $findpwd_form.style.display = 'none';
                    $printpwd_form.style.display = "block";
                }
            })
            .catch((Error) => {
                console.error('Error:', Error); // 에러 처리
            });
        }
    });  

    //비밀번호를 확인했고 로그인 페이지로 넘어가기 위한 확인 버튼
    $pwdfindokbtn.addEventListener('click', ()=>{
        const pwd = $member_pwd.value;
        const check_pwd = $checkmember_pwd.value;
        
        if (pwd == "") {
            alert("비밀번호를 입력하세요");
            return;
        }  
        if (check_pwd == "") {
            alert("비밀번호 확인에 비밀번호를 입력하세요");
            return;
        }
        if (pwd === check_pwd) {
            fetch(`/newpwd`, {
                method : 'POST',
                headers : { "Content-Type" : "application/json" },
                body : JSON.stringify({"member_id" : pwdid,"member_password" : pwd})
            })
            .then((message) => { return message.text()})
            .then((message) => {
                if(message == "fails") {
                    alert(`${pwdid}로 비밀번호를 찾을 수 없습니다.`);
                }
                else {
                    $findpwd_form.style.display = 'none';
                    $printpwd_form.style.display = "block";
                }
            })
            .catch((Error) => {
                console.error('Error:', Error); // 에러 처리
            });
        }
        else {
            alert("비밀번호가 다릅니다.");
        }
    });
})();