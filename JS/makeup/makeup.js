// 버튼을 클릭 시 중복 클릭을 막기위해 클릭한 것을 나타내기 위한 함수
function check_numberbtn(numbutton) {
    // 일단 모든 버튼을 사용할 수 있게 변경
    $save_1.disabled = false;
    $save_2.disabled = false;
    $save_3.disabled = false;
    $save_4.disabled = false;
    $save_5.disabled = false;

    $save_1.style.opacity = 1;
    $save_2.style.opacity = 1;
    $save_3.style.opacity = 1;
    $save_4.style.opacity = 1;
    $save_5.style.opacity = 1;

    // 그러고 나서 입력 받은 버튼을 사용할 수 없게 변경
    numbutton.disabled = true;
    numbutton.style.opacity = 0.2;
}

$savenumber.forEach(button => {
    button.addEventListener('click', ()=>{
        const btnid = button.id;
        const btnnum = btnid.split('_')[1];
        isNumberClick = true;               // 사용자가 저장하기 전에 숫자 버튼을 클릭했는지 확인하기 위한 boolean
        whatNumber = btnnum;
        check_numberbtn(button);   // 버튼을 사용할 수 없게 변경
    });
});

function sendDataMakeup(slider, category, whatColor) {
    fetch(`/savemakeup`, {
        method : 'POST',
        headers : { "Content-Type" : "application/json" },
        body : JSON.stringify({"number" : whatNumber, "opacity" : slider, "color_code" : whatColor, "category" : category})
    })
    .catch((Error) => {
        console.error('Error:', Error); // 에러 처리
    });
}

$savebtn.addEventListener('click', ()=>{
    if(isNumberClick == true) {
        sendDataMakeup(Fdslider, "fundation", FdwhatColor);
        sendDataMakeup(Lipslider, "lipstick", LipwhatColor);
        // sendDataMakeup(EyeLineslider, "eyeline", EyeLinewhatColor);
    }
    else {
        alert('저장할 버튼을 클릭해주세요');
    }
});

//////////// 카메라 부분 //////////////
let connectCam = false;     // 현재 캠이 연결되었는지 확인 false : 미연결 true : 연결
const $CamBtn = document.getElementById('CamBtn');      // 카메라 연결과 해제를 위한 버튼
const $video = document.getElementById('video');         // 카메라를 보이게 하는 영역

//////////// 웹 소켓 함수 부분 //////////////
function cunnectWebsocket() {
    const websocket = new WebSocket('ws://127.0.0.1:8080/video-feed');
    websocket.onmessage = function(event) {
        const blob = new Blob([event.data], { type: 'image/jpeg' });
        const url = URL.createObjectURL(blob);
        $video.src = url;
    };
}

///////////// python 프로세스 연결 //////////////
function sendConnectPython() {
    fetch('/practice', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then((message)=>{ return message.text() })
    .then((message)=>{
        if(message == "already") {    // 컨트롤러에서 중복인지 아닌지 판단하면서 text를 전송하는데 exist면 중복
            alert(`이미 실행 중 입니다.`);
        }
        else {
            alert('프로그램이 실행합니다.');
        }
    })
    .catch(error => {
        alert('/practice: 네트워크 오류가 발생했습니다: ' + error);
    });
}
///////////// python 프로세스 종료 //////////////
function sendDestroyPython() {
    fetch('/shutdown', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then((message)=>{ return message.text() })
    .then((message)=>{
        if(message == "already") {    // 컨트롤러에서 중복인지 아닌지 판단하면서 text를 전송하는데 exist면 중복
            alert(`이미 종료되었습니다. 입니다.`);
        }
        else {
            alert('프로그램이 종료됩니다.');
        }
    })
    .catch(error => {
        alert('/shutdown: 네트워크 오류가 발생했습니다: ' + error);
    });
}

// 색상 이름과 HEX 값을 매핑하는 Map 객체 생성
const colorMap = new Map([
    ['red', '#ff0000'],
    ['green', '#00ff00'],
    ['blue', '#0000ff'],
    ['yellow', '#ffff00'],

    ['orange', '#ff7f00'],
    ['purple', '#800080'],
    ['pink', '#ffc0cb'],
    ['cyan', '#00ffff'],
    
    ['brown', '#a52a2a'],
    ['gray', '#808080'],
    ['lightcoral', '#f08080'],
    ['lightgreen', '#90ee90'],

    ['lightblue', '#add8e6'],
    ['lavender', '#e6e6fa'],
    ['gold', '#ffd700'],
    ['salmon', '#fa8072'],

    ['teal', '#008080'],
    ['navy', '#000080'],
    ['maroon', '#800000'],
    ['olive', '#808000'],

    ['coral', '#ff7f50'],
    ['plum', '#dda0dd'],
    ['khaki', '#f0e68c'],
    ['chocolate', '#d2691e'],

    ['sienna', '#a0522d'],
    ['slateblue', '#6a5acd'],
    ['mediumseagreen', '#3cb371'],
    ['lightsalmon', '#ffa07a'],
    
    ['lightgray', '#d3d3d3'],
    ['darkorange', '#ff8c00'],
    ['springgreen', '#00ff7f'],
    ['violet', '#ee82ee'],
]);

// 파운데이션 바르기 버튼을 클릭했을 경우
$showFdMakeupSelectBox.addEventListener('click', ()=>{
    $SelectMakeupButton.style.display = 'none';    // 버튼들 안보이게 하기
    $MakeupSelectBox.style.backgroundColor = '#339adf';
    $MakeupSelectBox.style.display = "block"; // 셀렉트 박스 보이게 하기 height: 480px
    $MakeupSelectBox.style.height = '480px';
    $foundation.style.display = 'block';
    $sliderValue.value = Fdslider;
    $colorBox1.style.backgroundColor = FdwhatColor;
    whatBtn = 'Fd';
});

// 립 바르기 버튼을 클릭했을 경우
$showLipMakeupSelectBox.addEventListener('click', ()=>{
    $SelectMakeupButton.style.display = 'none';    // 버튼들 안보이게 하기
    $MakeupSelectBox .style.backgroundColor = '#ec7b7b';
    $MakeupSelectBox.style.height = '350px';
    $MakeupSelectBox.style.display = "block"; // 셀렉트 박스 보이게 하기
    $lip.style.display = 'block';
    $sliderValue.value = Lipslider;
    $colorBox2.style.backgroundColor = LipwhatColor;
    whatBtn = 'Lip';
});

// // 아이라인 바르기 버튼을 클릭했을 경우
// $showEyeLineMakeupSelectBox.addEventListener('click', ()=>{
//     $SelectMakeupButton.style.display = 'none';    // 버튼들 안보이게 하기
//     $MakeupSelectBox.style.backgroundColor = '#362349';
//     $MakeupSelectBox.style.display = "block"; // 셀렉트 박스 보이게 하기
//     $sliderValue.value = EyeLineslider;
//     whatBtn = 'EyeLine';
// });

// 셀렉터 박스에서 닫기 버튼을 클릭했을 경우
$closeBtn.addEventListener('click', ()=>{
    $MakeupSelectBox.style.display = "none";    // 셀렉트 박스 안보이게 하기
    $foundation.style.display = 'none';
    $lip.style.display = 'none';
    $SelectMakeupButton.style.display = 'block';   // 버튼들 보이게 하기   
});

function colorevent(color) {
    /////////////////// 버튼 값 POST로 전송 ///////////////////
    fetch(`/Color?whatBtn=${whatBtn}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'color_code' : color })
    });
}
// 셀렉터의 색상 중 하나를 클릭했을 경우 실행되는 동작
$color_button.forEach(button => {
    button.addEventListener('click', () => {

        const color = colorMap.get(button.style.backgroundColor); // 색상 추출
        if(whatBtn == "Fd") {
            $colorBox1.style.backgroundColor = color;
            $colorBox1.style.backgroundImage = "none";
            FdwhatColor = color;
        }
        else if(whatBtn == "Lip") {
            $colorBox2.style.backgroundColor = color;
            $colorBox2.style.backgroundImage = "none";
            LipwhatColor = color;
        }
        // else if(whatBtn == "EyeLine") {
        //     EyeLinewhatColor = color;
        // }
        colorevent(color);
    });
});

// 투명도 슬라이더를 드래그할 경우 발생하는 동작
function sliderevent (value) {
    ////////////////// 슬라이더 값 POST로 전송 ///////////////////
    fetch(`/Slider?whatBtn=${whatBtn}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'opacity' : value })
    });
    if(whatBtn == "Fd") {
        Fdslider = value;
    }
    else if(whatBtn == "Lip") {
        Lipslider = value;
    }
    // else if(whatBtn == "EyeLine") {
    //     EyeLineslider = value;
    // }
};


cunnectWebsocket();
$CamBtn.addEventListener('click', ()=>{
    if(connectCam === false) {   // 캠 미연결이므로 연결 동작 실행
        cunnectWebsocket();
        sendConnectPython();
        cunnectWebsocket();
         
        $video.style.backgroundImage = 'url(http://localhost:8080/video_feed)'; // 캠 스트림 URL 설정
        $video.style.display = 'block';   // 비디오 부분 보이게 설정
        $CamBtn.textContent = '카메라 해제';    // 연결되어 있으므로 연결을 해제 위해 카메라 해제로 명칭 변경
        $SelectMakeupButton.style.display = 'block';
        connectCam = true;
    }
    else {  // 캠이 연결되어 있으니 해제 동작 실행
        sendDestroyPython();
        $CamBtn.textContent = '카메라 연결';    // 연결 해제되므로 다시 연결을 위해 카메라 연결로 명칭 변경
        $SelectMakeupButton.style.display = 'none';
        streamActive = false; // 상태 업데이트
        $video.style.display = 'none';
        connectCam = false;
    }
});