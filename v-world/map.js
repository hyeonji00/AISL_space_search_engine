var vmap;                                                                           // 기본 지도를 받을 변수
var markerLayer;                                                                    // 마커 레이어를 받을 변수
var x,y;                                                                            // 클릭한 위경도를 받을 변수
var checkRoadView = false;
var key = "인증키";                                   // 브이월드 인증키
var titleName;                                                                      // 마커에 표시될 검색방법 타이틀


// 서울역 14134490.6 76941859, 4516889.004840847

vw.ol3.CameraPosition.center = [14145868.603246644, 4516117.737187111];             // 기본 지도 시작 중심 좌표 지정(세종대)
vw.ol3.CameraPosition.zoom = 17;                                                    // 시작 Zoom 레벨

vw.ol3.MapOptions = {                                                               // 기본지도의 옵션
    basemapType: vw.ol3.BasemapType.GRAPHIC
, controlDensity: vw.ol3.DensityType.EMPTY
, interactionDensity: vw.ol3.DensityType.BASIC
, controlsAutoArrange: true
, homePosition: vw.ol3.CameraPosition
, initPosition: vw.ol3.CameraPosition
}; 
    
vmap = new vw.ol3.Map("vMap",  vw.ol3.MapOptions);                                  // 기본 지도 생성  


// 지도 클릭 이벤트
vmap.on('click', function(event) {
    
    var feature = vmap.forEachFeatureAtPixel(event.pixel, function (feature,layer) {// 클릭한 좌표를 첫번째 인자로 주어 해당 위치에 있는 feature를 구하고 두번쨰 인자(함수)로 넘겨준다.
        if(layer != null && layer.className == 'vw.ol3.layer.Marker'){              // 해당 좌표에 마커 레이어가 있다면
            return feature;
        }else{
            return false;
        }
    });
    
    if (!feature) {
        var coord = vmap.getCoordinateFromPixel(event.pixel);                       // 마우스 커서 아래의 좌표값 구하기
        x = coord[0];
        y = coord[1];
        if(checkRoadView){                                                          // 로드뷰 실행
            var tansform = ol.proj.transform([x,y], 'EPSG:3857', 'EPSG:4326')       // 브이월드 좌표계에서 다음 지도 좌표계로 변환 EPSG:3857=>EPSG:4326
            location.href="https://map.kakao.com/link/roadview/"+tansform[1]+","+tansform[0];   // 로드뷰 불러오기
        }else{
            addMarker(x, y);                                                        // addMarker함수에 위경도 변수 넘기고 실행
            var tansform = ol.proj.transform([x,y], 'EPSG:3857', 'EPSG:4326')
            console.log("v-world 좌표 :\n", x, y, "\n위도, 경도 :\n", tansform[0], tansform[1])

        }
    }
});


function addMarker(lon ,lat) {
    vmap.removeLayer(markerLayer);                                          // 기존의 마커가 있다면 제거
    markerLayer = new vw.ol3.layer.Marker(vmap);                            // 마커 객체 상성

    var typeName = $('.search_type option:selected').val();                 // 선택한 검색 종류 값

    if(typeName == "road"){titleName = "도로명 주소";}
    else if(typeName == "parcel"){titleName = "지번 주소";}

    //  (비동기)좌표를 주소로 변환하는 api, 도로명주소 검색의 경우 건물의 geometry 기반으로 도로명 주소값을 가지고 오기 때문에 
    //  건물 외의 것을 클릭하면 값이 없을 수 있습니다. 
    //  브이월드 지도서비스에서 행정 주제도중 도로명주소건물 주제도에 해당 좌표값이 들어와야만 도로명 주소값을 리턴 받을 수 있습니다.
    $.ajax({ 
        type: 'GET',
        url: 'http://api.vworld.kr/req/address?',
        dataType : "jsonp",                                                 // CORS 문제로 인해 브이월드에선 jsonp를 사용한다고 함
        data: {
            service: "address",
            version: "2.0",
            request: "getaddress",
            format: "json",                                                 // 결과 포멧으로 xml 또는 json 타입으로 받아볼 수 있다.
            key: key,                                                       // 브이월드 인증키
            type: typeName,                                                 // 검색 타입으로 '도로명:road' 또는 '지번:parcel' 또는 '둘다:both' 중 선택
            crs: "epsg:3857",                                               // 브이월드 기본 좌표계
            point: lon+","+lat,                                             // 좌표
            zipcode: true,                                                  // 우편번호 여부
            simple: false                                                   // 간략 결과 여부
        },
        success: function(json_data){
            if(json_data.response.status == "NOT_FOUND"){
                text = "검색 결과가 없습니다.";
            }else{
                text = json_data.response.result[0].text;                   // 받아온 json데이터에서 주소를 추출
            }
            
            vw.ol3.markerOption = {                                         // 마커 옵션 설정
                x : lon,
                y : lat,
                epsg : "EPSG:3857",
                title : titleName,
                contents : text,
                iconUrl : 'http://map.vworld.kr/images/ol3/marker_blue.png'
            };
            markerLayer.addMarker(vw.ol3.markerOption);                     // 마커 옵션을 마커에 적용
            vmap.addLayer(markerLayer);                                     // 마커를 vmap에 등록
        },
        error: function(xtr,status,error){
            alert(xtr +" : "+status+" : "+error);
        }
    });
};



// 지도 검색
$('.search_btn').on('click',function(){

    vmap.removeLayer(markerLayer);                              // 기존의 마커 제거
    markerLayer = new vw.ol3.layer.Marker(vmap);                // 마커 객체 상성

    var contents_data;
    var typeName = $('.search_type option:selected').val();     // 선택한 검색 종류 값
    
    $.ajax({
        type: "get",
        url: "http://api.vworld.kr/req/search",
        data : {
            page: 1,
            type: 'address',                                    // 주소 검색방법
            category: typeName,                                 // 도로명 : road, 지번 : parcel
            request: 'search',
            apiKey: key,                                        // 브이월드 지도 인증기
            domain: '본인의 map을 보여주는 도메인 ex) http://111.111.111.111/map.html',
            crs : 'EPSG:3857',                                  // 브이월드 좌표계
            query : $('#search').val()                          // 사용자가 입력한 text
        },
        dataType: 'jsonp',
        async: false,
        success: function(data) {
            if(data.response.status =="NOT_FOUND"){
                alert("검색결과가 없습니다.");
            }else{
                for(var o in data.response.result.items){ 
                    if(o==0){
                        move(data.response.result.items[o].point.x*1,data.response.result.items[o].point.y*1);
                        if(typeName == "road"){
                            titleName = "도로명 주소";
                            contents_data = data.response.result.items[o].address.road;
                        }
                        else if(typeName == "parcel"){
                            titleName = "지번 주소";
                            contents_data = data.response.result.items[o].address.parcel;
                        }
                    }

                    vw.ol3.markerOption = {                                         // 마커 옵션 설정
                        x : data.response.result.items[o].point.x,
                        y : data.response.result.items[o].point.y,
                        epsg : "EPSG:3857",
                        title : titleName,
                        contents : contents_data,
                        iconUrl : 'http://map.vworld.kr/images/ol3/marker_blue.png'
                    };

                    markerLayer.addMarker(vw.ol3.markerOption);                  // 마커 옵션을 마커에 적용
                }
            }
        },
        complete:function(){
            vmap.addLayer(markerLayer)                                   // 마커를 vmap에 등록
        },
        error: function(xhr, status, error) {
            console.log(xhr, status, error);
        }
    });
    var move = function(x,y){
        vmap.getView().setCenter([ x, y ]); // 지도 이동
        vmap.getView().setZoom(17);         // 줌레벨 설정
    }
});