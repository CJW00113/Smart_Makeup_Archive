(()=>{
    const $checkbtn = document.getElementById("checkbtn");
        const $pwd = document.getElementById("pwd");

        // 버튼을 클릭 시
        $checkbtn.addEventListener('click', ()=>{
            const pwd = $pwd.value;

            fetch(`/checkpassword`, {
                method : 'POST',
                headers : { "Content-Type" : "application/json" },
                body : JSON.stringify({"member_password" : pwd})
            })
            .then((message)=>{ return message.text() })
            .then((message)=>{
                if(message == "fails") {    // 컨트롤러에서 비밀번호가 맞는지 확인한 결과
                    alert(`잘못된 비밀번호입니다.`);
                }
                else {
                    window.location.href = `/profile`;
                }
            });
        });

        // 엔터키 눌렀을 때
        $pwd.addEventListener('keypress', (event)=>{
            if(event.key == 'Enter') {
                event.preventDefault();
                const pwd = $pwd.value;

                fetch(`/checkpassword`, {
                    method : 'POST',
                    headers : { "Content-Type" : "application/json" },
                    body : JSON.stringify({"member_password" : pwd})
                })
                .then((message)=>{ return message.text() })
                .then((message)=>{
                    if(message == "fails") {
                        alert(`잘못된 비밀번호입니다.`);
                    }
                    else {
                        window.location.href = `/profile`;
                    }
                });
            }
        });
})();