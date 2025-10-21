function openNav() {
    document.getElementById("sidebar").style.width = "30%";
    document.getElementById("main").style.marginLeft = "30%";

    fetch(`/characters`)
        .then(response => {
            if (!response.ok) {
                throw new Error('網路出現問題');
            }
            return response.json();
        })
        .then(data => {
            if (data !== null) {
                document.getElementById("character-name").innerHTML = '名稱：' + data.name;
                document.getElementById("character-profession").innerHTML = '職業：' + data.occupation;
                document.getElementById("character-level").innerHTML = '等級：' + data.level;
                document.getElementById("character-exp").innerHTML = '經驗：' + data.experience;
                document.getElementById("character-partners").innerHTML = '夥伴：' + data.partner;
            } else {
                document.getElementById("character-name").innerHTML = "查無此人";
            }
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        }
    );


    document.getElementById("searchForm").style.display = "none";


    document.getElementById("uploadButton").style.display = "none";
    document.getElementById("menuIcon").onclick = function(){closeNav()};
    document.getElementById("menuIcon").innerHTML = "<";

}

function closeNav() {
    document.getElementById("sidebar").style.width = "0";
    document.getElementById("main").style.marginLeft= "0";

    // 檢查使用者身分狀態，若為上傳者則隱藏搜尋欄
    if (document.getElementById("userSwitch").checked) {
        document.getElementById("uploadButton").style.display = "Block";
    }
    else
    {
        document.getElementById("searchForm").style.display = "Block";
    }
    document.getElementById("menuIcon").onclick = function(){openNav()};
    document.getElementById("menuIcon").innerHTML = ">";
}