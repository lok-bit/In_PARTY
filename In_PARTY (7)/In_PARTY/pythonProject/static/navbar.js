document.addEventListener('DOMContentLoaded', function() {
        const userAvatar = document.getElementById('userAvatar');
        const dropdownContent = document.getElementById('dropdownContent');

        // 點擊頭像時切換下拉式選單的顯示狀態
        userAvatar.addEventListener('click', function() {
            dropdownContent.classList.toggle('show');
        });

        // 點擊頁面上其他位置時隱藏下拉式選單
        window.addEventListener('click', function(event) {
            if (!event.target.matches('.user-avatar')) {
                dropdownContent.classList.remove('show');
            }
        });
});
