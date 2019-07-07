$(document).ready(function() {

    function clearRightPanelList() {
        $('.right-panel-list').empty();
    }

    function clearEditPanelOptionsPanel() {
        $('.editPanelOptions').empty();
    }

    function addTestCaseEditPanelOptions() {
        $('.editPanelOptions').append('<button type="button" class="btn btn-outline-dark editPanelOptionButton">Add Script to Repo</button>');
        $('.editPanelOptions').append('<button type="button" class="btn btn-outline-dark editPanelOptionButton">Remove Script From Repo</button>');
        $('.editPanelOptions').append('<button type="button" class="btn btn-outline-dark editPanelOptionButton">Remove Script From Execution Queue</button>');
        $('.editPanelOptions').append('<button type="button" class="btn btn-outline-dark editPanelOptionButton">Run Selected Scripts</button>');
        attachEditPanelViewControllers();
    }

    function addDeviceEditPanelOptions() {
        $('.editPanelOptions').append('<button type="button" class="btn btn-outline-dark editPanelOptionButton">Add Device to Repo</button>');
        $('.editPanelOptions').append('<button type="button" class="btn btn-outline-dark editPanelOptionButton">Remove Device From Repo</button>');
        $('.editPanelOptions').append('<button type="button" class="btn btn-outline-dark editPanelOptionButton">Attach Devices to Tests</button>');
        attachEditPanelViewControllers();
    }

    //////////////////////////////////////////////////////////////////////////////////////////////////////
    //Button action controllers/ AJAX requests occur here
    //////////////////////////////////////////////////////////////////////////////////////////////////////
    addControllers();

    function attachDeviceButtonController() {
        $('.device-button').on('click', function(event) {
            $.ajax({
                    data: {
                        repository: 'device_repository'
                    },
                    type: 'POST',
                    url: '/selectionPanelResponse'
                })
                .done(function(data) {

                    clearRightPanelList();
                    clearEditPanelOptionsPanel();
                    addDeviceEditPanelOptions();

                    for (var i = 0; i < data.length; i++) {
                        $('.right-panel-list').append(' <a href="#" class="list-group-item list-group-item-action">' + data[i] + '</a>');
                    }
                });
            event.preventDefault();
        });

    }

    function attachTestCaseButtonController() {
        $('.test-case-button').on('click', function(event) {
            $.ajax({
                    data: {
                        repository: 'test_case_repository'
                    },
                    type: 'POST',
                    url: '/selectionPanelResponse'
                })
                .done(function(data) {

                    clearRightPanelList();
                    clearEditPanelOptionsPanel();
                    addTestCaseEditPanelOptions();

                    for (var i = 0; i < data.length; i++) {
                        $('.right-panel-list').append(' <a href="#" class="list-group-item list-group-item-action testCaseListItem">' + data[i] + '</a>');
                    }
                });

            event.preventDefault();
        })

    }

    function attachSavedResultsButtonController() {

        $('.saved-results-button').on('click', function(event) {
            clearEditPanelOptionsPanel();
            $('.editPanelView').empty();
            $.ajax({
                    data: {

                    },
                    type: 'POST',
                    url: '/updateDatabase'
                })
                .done(function(data) {
                    $('.results-table tbody').empty();

                    for (let i = 0; i < data.database.length; i++) {
                        $('.results-table tbody').append('<tr><td>' + data.database[i][0] + '</td><td>' + data.database[i][1] + '</td><td>' + data.database[i][2] + '</td><td></td></tr>');
                    }


                });
        });
    }

    function attachEditPanelViewControllers() {
        $('.editPanelOptionButton').on('click', function(event) {
            switch ($(this).text().trim()) {
                case 'Add Script to Repo':
                    $('.editPanelView').empty();
                    exitRemoveScriptMode();
                    AddEditPanelOptions();
                    AddScriptToRepo();
                    break;
                case 'Remove Script From Repo':
                    $('.editPanelView').empty();
                    exitRemoveScriptMode();
                    RemoveScriptFromRepo();
                    break;
                case 'Remove Script From Execution Queue':
                    $('.editPanelView').empty();
                    exitRemoveScriptMode();

                    break;
                case 'Run Selected Scripts':
                    $('.editPanelView').empty();
                    exitRemoveScriptMode();
                    RunSelectedScripts();
                    break;
            }
        });
    }

    function RunSelectedScripts() {
        $('.editPanelView').append('<div class="form-group"><label for="ExecuteList">Scripts for Execution Queue</label><select multiple class="form-control executeList" id="ExecuteList"></select><br /><button type="submit" class="btn btn-dark executeButton">Execute</button></div>');

        executeButtonController();

        listUpdater('executeList');
    }

    function RemoveScriptFromQueue() {

    }

    function AddEditPanelOptions() {
        $('.editPanelView').append('<div class="form-group"><label for="scriptName"></label><input type="text" class="form-control add-input" id="scriptName" placeholder="Script Name"></div>');
        $('.editPanelView').append('<form><div class="form-group add-file"><label for="scriptSelection"></label><input type="file" class="form-control-file" id="scriptSelection"></div></form>');
        $('.editPanelView').append('<input class="btn btn-dark add-submit" type="submit" value="Submit">');
    }

    function AddScriptToRepo() {

        function loadSubmitController(script, scriptname) {

            $('.add-submit').on('click', function(event) {
                let scriptName = $('#scriptName').val().trim();
                let scriptLocation = $('#scriptSelection').val().trim();

                $.ajax({
                        data: {
                            _script: script,
                            _scriptName: scriptName
                        },
                        type: 'POST',
                        url: '/userGeneratedScriptUploading'
                    })
                    .done(function(data) {
                        $('.right-panel-list').append('<a href="#" class="list-group-item list-group-item-action">' + data.name + '</a>');

                    });
            });
        }

        $('#scriptSelection').on('change', function(event) {
            let file = event.target.files;
            let reader = new FileReader();

            reader.onload = function(event) {
                let script = event.target.result;
                let scriptName = $('#scriptSelection').val().trim();

                loadSubmitController(script, scriptName);

            }
            reader.readAsText(file[0]);

        });
    }

    let selectionArray = [];

    function exitRemoveScriptMode() {
        selectionArray = [];
        $('.right-panel-list *').each(function() {
            if ($(this).hasClass('selectedListItem')) {
                $(this).removeClass('selectedListItem');
            }
        });
    }

    function RemoveScriptFromRepo() {
        // window.alert('please select the script(s) for removal');
        $('.editPanelView').append('<div class="form-group"><label for="DeleteList">Scripts for Deletion</label><select multiple class="form-control deleteList" id="DeleteList"></select><br /><button type="submit" class="btn btn-dark deleteButton">Delete</button></div>');
        deleteButtonController();
        listUpdater('deleteList');
    }

    function listUpdater(list) {

        $('.testCaseListItem').on('click', function(event) {
            if ($(this).hasClass('selectedListItem')) {
                $(this).removeClass('selectedListItem');
                index = selectionArray.indexOf($(this).text().trim());
                selectionArray.splice(index, 1);
            } else {
                $(this).addClass('selectedListItem');
                selectionArray.push($(this).text().trim());
            }

            $('.' + list).empty();

            for (let i = 0; i < selectionArray.length; i++) {
                $('.' + list).append('<option>' + selectionArray[i] + '</option>');
            }

        });

    }

    function deleteButtonController() {
        $('.deleteButton').on('click', function(event) {
            dataSend = JSON.stringify(selectionArray);

            $.ajax({
                    data: {
                        scriptslist: dataSend
                    },
                    type: 'POST',
                    url: '/removeScriptsFromRepo'
                })
                .done(function(data) {
                    window.alert('Scripts Deleted.');
                    $('.deleteList').empty();

                    $('.right-panel-list *').each(function() {
                        if ($(this).hasClass('selectedListItem')) {
                            $(this).remove();
                        }
                    });
                });
        });
    }

    function executeButtonController() {
        $('.executeButton').on('click', function(event) {
            dataSend = JSON.stringify(selectionArray);

            $.ajax({
                    data: {
                        scriptslist: dataSend
                    },
                    type: 'POST',
                    url: '/executeScripts'
                })
                .done(function(data) {
                    // window.alert(data.ret);
                    $('.executeList').empty();
                });
        });
    }


    /////////////////////////////////////////////////////////////////////////////////////////////////////
    //
    /////////////////////////////////////////////////////////////////////////////////////////////////////

    function addControllers() {
        attachDeviceButtonController();
        attachTestCaseButtonController();
        attachSavedResultsButtonController();
    }
});