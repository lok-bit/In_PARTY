function popMarkerInfo(id) {
    fetch(`/activity_info?id=${id}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('網路出現問題');
            }
            return response.json();
        })
        .then(data => {
            if (data !== null) {
                document.getElementById("name").innerHTML = data.name;
                document.getElementById("markercontant").innerHTML = data.content;
                document.getElementById("linker").href = data.url;
                document.getElementById('markerimg').src = `static/image/${data.image_name}`;
                document.getElementById("markerstartdate").innerHTML = data.date_start;
                document.getElementById("markerenddate").innerHTML = data.date_end;
                document.getElementById("markerlocation").innerHTML = "活動地點：" + data.address;
                document.getElementById("markercount").innerHTML = "活動人數：" + data.count;
                console.log("111");
                console.log(data.info);
                showJoinButton(data.id, data.info);
                if (data.info != null){
                    if (data.info.type == "0" && data.info.check_in == "True"){
                        document.getElementById("toggleScannerWindow").style.display = 'none';
                        document.getElementById("openScannerWindow").style.display = 'block';
                    }else if(data.info.type != "0"){
                        document.getElementById("toggleScannerWindow").style.display = 'block';
                        document.getElementById("openScannerWindow").style.display = 'none';
                    }else{
                        document.getElementById("toggleScannerWindow").style.display = 'none';
                        document.getElementById("openScannerWindow").style.display = 'none';
                    }
                }else{
                    document.getElementById("toggleScannerWindow").style.display = 'none';
                    document.getElementById("openScannerWindow").style.display = 'none';
                }
            } else {
                document.getElementById("name").innerHTML = "查無此活動";
            }
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
    openMarkerinf();

    function joinHandler(id, flag) {
        const endpoint = flag ? `/disjoin?id=${id}` : `/join?id=${id}`;
        console.log(id);
        console.log(flag);
        fetch(endpoint)
            .then(response => {
                if (!response.ok) {
                    throw new Error('網路出現問題');
                }
                return response.json();
            })
            .then(data => {
                console.log(data);
                if (data != null && data.result) {
                    return popMarkerInfo(id);
                }
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            });
    
        // 在此處返回false，表示此事件處理函式是異步的
        return false;
    }

    function hold(id, flag) {
        const endpoint = flag ? `/cancel?id=${id}` : `/check_in?id=${id}`;
        console.log(id);
        fetch(endpoint)
        .then(response => {
            if (!response.ok) {
                throw new Error('網路出現問題');
            }
            return response.json();
        })
        .then(data => {
            if (data != null && data.result) {
                return popMarkerInfo(id);
            }
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });

        return false;
    }

    function showJoinButton(id, info) {
        console.log(id);
        var flag;
        var flag2;
        if(info != null && info.type == "0"){
            flag = info != null ? info.check_in == "True" : false;
            flag2 = true;
        }else{
            flag = info != null ? true : false;
            flag2 = false;
        }
        const joinButton = document.getElementById('join');
        joinButton.textContent = flag ? "取消" : "活動";
        joinButton.textContent += flag2 ? "舉辦" : "參加";
        joinButton.onclick = flag2 ? function(){hold(id, flag)} : function(){joinHandler(id, flag)};
    }
}
function printjoin(){
    document.getElementById("join").style.display = "block";
    let joining = document.getElementById("join");
    joining.innerHTML = "<a>點選參加活動</a>"
}
function openMarkerinf() {
    document.getElementById("markerinf").style.width = "30%";
    console.log('open');
}

function closeMarkerinf() {
    document.getElementById("markerinf").style.width = "0";
    
}

