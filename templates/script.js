// AJAX 请求获取病人数据
function loadPatients() {
    $.ajax({
        url: '/patients',
        method: 'GET',
        success: function(data) {
            let patientsTableBody = $('#patients-table tbody');
            patientsTableBody.empty();
            data.forEach(patient => {
                patientsTableBody.append(`
                    <tr>
                        <td>${patient.Name}</td>
                        <td>${patient.Gender}</td>
                        <td>${patient.Age}</td>
                        <td>${patient.Address}</td>
                        <td><button class="btn-info">详情</button></td>
                    </tr>
                `);
            });
        },
        error: function() {
            alert("无法加载病人信息");
        }
    });
}

// AJAX 请求获取病房数据
function loadWards() {
    $.ajax({
        url: '/wards',
        method: 'GET',
        success: function(data) {
            let wardsTableBody = $('#wards-table tbody');
            wardsTableBody.empty();
            data.forEach(ward => {
                wardsTableBody.append(`
                    <tr>
                        <td>${ward.Location}</td>
                        <td>${ward.RoomTypeCode}</td>
                        <td>${ward.FeeStandard}</td>
                        <td>${ward.Status}</td>
                        <td><button class="btn-info">详情</button></td>
                    </tr>
                `);
            });
        },
        error: function() {
            alert("无法加载病房信息");
        }
    });
}

// 页面加载完成后自动加载数据
$(document).ready(function() {
    loadPatients();
    loadWards();
});
