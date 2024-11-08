//////////// 셀렉트 박스 부분 //////////////
const $SelectMakeupButton = document.getElementById('SelectMakeupButton');                      // 셀렉트 박스 버튼 전체 부분
const $showFdMakeupSelectBox = document.getElementById('showFdMakeupSelectBox');                // 파운데이션 바르기 버튼
const $showLipMakeupSelectBox = document.getElementById('showLipMakeupSelectBox');              // 립 바르기 버튼
const $showEyeLineMakeupSelectBox = document.getElementById('showEyeLineMakeupSelectBox');      // 아이라인 버튼
const $MakeupSelectBox = document.getElementById('MakeupSelectBox');                            // 셀렉트 박스
const $colorBox1 = document.getElementById('colorBox1');                                          // 셀렉트 박스에 있는 색상 박스
const $colorBox2 = document.getElementById('colorBox2');                                          // 셀렉트 박스에 있는 색상 박스
const $color_button = document.querySelectorAll('.color-button');                                // 셀렉터에 존재하는 색상들을 전부 불러오기
const $closeBtn = document.getElementById('closeBtn');                                          // 셀렉터 닫기 버튼
const $sliderValue = document.getElementById('sliderValue');                                    // 투명도를 위한 슬라이더 값
                                                                                  
const $foundation = document.getElementById('foundation');                                       // 파운데이션인지 립인지 아이라인인지 구분하기 위한 변수
const $lip = document.getElementById('lip');
const $loadbtn = document.getElementById('loadbtn');

const $savenumber = document.querySelectorAll('[id^="save_"]');
const $save_1 = document.getElementById('save_1');
const $save_2 = document.getElementById('save_2');
const $save_3 = document.getElementById('save_3');
const $save_4 = document.getElementById('save_4');
const $save_5 = document.getElementById('save_5');
const $savebtn = document.getElementById('savebtn');

// 사용자가 어디에 화장 정보를 저장할 건지에 대한 버튼
let isNumberClick = false;
let whatNumber = 1;

// 어느 부위를 선택한건지를 나타내는 버튼
let whatBtn; 

// 부위별 투명도를 조절하기 위한 슬라이더 값
let Fdslider = 0;
let Lipslider = 0;
let EyeLineslider = 0;

// 화장품 종류별 색상
let FdwhatColor = "#00000000";
let LipwhatColor = "#00000000";
let EyeLinewhatColor = "#00000000";