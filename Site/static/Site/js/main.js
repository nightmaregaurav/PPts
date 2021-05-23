let csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

const host_changed = (select) => {
    let host_id = select.value;
    host_id = parseInt(host_id);
    if (isNaN(host_id)){
        let tournament = $("#tournamentSelect")[0];
        let match = $("#matchSelect")[0];
        tournament.innerHTML = '<option value="initial" selected>Select Host First</option>';
        match.innerHTML = '<option value="initial" selected>Select Tournament First</option>';
        return false;
    }
    $.ajax({
        url: "/get-tournaments/" + host_id,
        timeout: 10000,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrfmiddlewaretoken,
        },
        beforeSend: function(_){
            showLoader();
        },
        success: function(result, status, _){
            let tournament = $("#tournamentSelect")[0];
            tournament.innerHTML = '<option value="initial" selected>Click to select</option>';
            // noinspection JSUnresolvedVariable
            for(let i=0; i<result.tournaments.length; i++){
                // noinspection JSUnresolvedVariable
                let t = result.tournaments[i];
                // noinspection JSUnresolvedVariable
                tournament.innerHTML += '<option value="' + t.id + '">' + t.display + ' (' + t.full + ')</option>';
            }
        },
        error: function(_, status, error){
            alert('Error occurred. Error status: ' + status + "; Error: " + error);
        },
        complete: function(_, __){
            hideLoader();
        },
    });
};
const tournament_changed = (select) => {
    let tournament_id = select.value;
    tournament_id = parseInt(tournament_id);
    if (isNaN(tournament_id)){
        let match = $("#matchSelect")[0];
        match.innerHTML = '<option value="initial" selected>Select Tournament First</option>';
        return false;
    }
    $.ajax({
        url: "/get-matches/" + tournament_id,
        timeout: 10000,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrfmiddlewaretoken,
        },
        beforeSend: function(_){
            showLoader();
        },
        success: function(result, status, _){
            let match = $("#matchSelect")[0];
            match.innerHTML = '<option value="initial" selected>Click to select</option>';
            // noinspection JSUnresolvedVariable
            if(result.match_list.length > 0){
                // noinspection JSUnresolvedVariable
                match.innerHTML += '<option value="' + result.match_list[0] + '">' + "Last(accumulated)" + '</option>';
            }
            let html = '';
            // noinspection JSUnresolvedVariable
            result.match_list.forEach(addOption);
            function addOption(item, _){
                html += '<option value="' + item + '">' + item + '</option>';
            }
            match.innerHTML += html;
        },
        error: function(_, status, error){
            alert('Error occurred. Error status: ' + status + "; Error: " + error);
        },
        complete: function(_, __){
            hideLoader();
        },
    });
};
const searchClicked = () => {
    let tournament = $("#tournamentSelect")[0].value;
    let match = $("#matchSelect")[0].value;
    tournament = parseInt(tournament);
    match = parseInt(match);
    if(!(isNaN(tournament) || isNaN(match))) {
        match = Math.abs(match);
        let tab = window.open('/' + tournament.toString() + '/' + match.toString(), '_blank');
        tab.focus();
    }
    else{
        alert('Select Proper Data First.');
        return false;
    }
};