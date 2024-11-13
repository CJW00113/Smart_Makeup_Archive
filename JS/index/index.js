(()=>{
    const $mainimg = document.getElementById("mainimg");
    
    const images = [
        '/sysimg/image1.png',
        '/sysimg/image2.png',
        '/sysimg/image3.png',
        '/sysimg/image4.png',
        '/sysimg/image5.png',
        '/sysimg/image6.png',
        '/sysimg/image7.png'
    ];
    let currentIndex = 0;


    setInterval(() => {
        const previousIndex = currentIndex;
        currentIndex = (currentIndex + 1) % images.length;
    
        $mainimg.classList.remove('active'); // 현재 이미지 숨기기
        $mainimg.src = images[currentIndex]; // 이미지 경로 변경
    
        $mainimg.onload = () => {
            $mainimg.classList.add('active'); // 이미지가 로드된 후 클래스 추가
        };
    
        // 이전 이미지가 로드되기 전에 active 클래스를 다시 추가하지 않도록 주의
        if (previousIndex !== currentIndex) {
            $mainimg.classList.remove('active'); // 항상 이전 이미지 숨기기
        }
    }, 5000);
    
})();