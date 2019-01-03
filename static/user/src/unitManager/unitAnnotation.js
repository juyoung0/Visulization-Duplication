/**
 * Created by dryji on 2017-02-20.
 * managing unit annotations integrated with its modal
 */
(function (parent) {
    _.extend(parent, {
        createUnitAnnotation: function ($block) {

            var obj = {
                username: userManager.USERNAME,
                project_name: userManager.PROJECT,
                session_name: userManager.SESSION,
                session_ver: userManager.SESSION_VER,
                block_iden: $block.data().req.block_iden,
                block_ver: $block.data().req.block_ver,
                author: $('input.input-author-note').val(),
                date: $('input.input-data-note').val(),
                data_annotation: $('textarea.input-data-note').val(),
                research_annotation: $('input:radio[name=confidence]:checked').val(),
                experiment_type: $('input.input-experiment-note').val(),
                platform_name: $('input.input-platform-note').val(),
                organism: $('input.input-organism-note').val()
            };
            return $.ajax({
                url: "createBlockAnnotation.html", method: 'post', data: {
                    username: userManager.USERNAME,
                    project_name: userManager.PROJECT,
                    session_name: userManager.SESSION,
                    session_ver: userManager.SESSION_VER,
                    block_iden: $block.data().req.block_iden,
                    block_ver: $block.data().req.block_ver,
                    block_annotation: JSON.stringify(obj)
                }, error: userManager.failAjax,
                success: function (data, status) {
                    //if (!data.success) return userManager.failAjax(data, status);
                    unitManager.btnAddUnitAnnotation(data, status);
                    unitManager.logger('Create-Unit-Annotation', {
                        username: userManager.USERNAME,
                        project_name: userManager.PROJECT,
                        session_name: userManager.SESSION,
                        session_ver: userManager.SESSION_VER,
                        block_iden: $block.data().req.block_iden,
                        block_name: $block.data().req.block_name,
                        block_ver: $block.data().req.block_ver,
                        block_annotation: JSON.stringify(obj)
                    });
                }
            });

        },
        btnAddUnitAnnotation: function (data, status) {
            //if (!data.success) return userManager.failAjax(data, status);


            $('#annotation-modal').modal('hide');
            unitManager.getAnnotations(unitManager.SELECTED.data().res.annotation_path);
        },
        getAnnotations: function (path, $block) {
            console.log(path);
            return $.ajax({
                url: path,
                method: 'POST',
                error: userManager.failAjax,
                success: function (data, status) {
                    //if (!data.success) return userManager.failAjax(data, status);
                    unitManager.addUnitAnnotation(data, status, $block)
                }
            })
        },
        addUnitAnnotation: function (data, status, $block) {
            //if (!data.success) return userManager.failAjax(data, status);
            //if (!data.success) return userManager.failAjax(data,status);
            if ($block == null) $block = unitManager.SELECTED;
            $block.find('.annotation-item').remove();
            var $anno = $block.find('.annotation');
            var $note;
            _.forEach(data.annotation_list, function (item, idx) {
                $note = $('<li class="annotation-item"><a data-trigger="hover click" data-toggle="popover" data-placement="right"><span class="badge">' + idx + '</span></a></li>');
                $anno.append($note);
                $note.find('a').attr('title', "<a class='btn btn-xs btn-danger delete-unit-annotation btn-block' id='anno-" + idx + "' onClick='unitManager.deleteUnitAnnotation(this)'>DELETE</div>");
                var regex = /\\n/g;
                var content = "<div class='badge'>Auhtor</div><pre>"
                    + item.annotation.author
                    + "</pre><div class='badge'>Date</div><pre>"
                    + item.annotation.date
                    + "</pre><div class='badge'>Answer</div><pre>"
                    + item.annotation.data_annotation.replace(regex, "\n")
                    + "</pre><div class='badge'>Confidence level</div><pre>"
                    + item.annotation.research_annotation.replace(regex, "\n") + "</pre>";

                $note.find('a').attr('data-content', content);
                $note.find('.delete-unit-annotation').on('click', function (e) {
                    console.log('delete', this, $(this).parent);
                });
                $note.find('a').on('click', function () {
                    $('[data-toggle="popover"]').popover('hide');
                    $(this).popover('toggle');
                });
            });
            $('[data-toggle="popover"]').popover({html: true});

        },
        deleteUnitAnnotation: function (item) {

            var idx = $(item).attr('id').split('-')[1];

            $.post("deleteBlockAnnotation.html", {
                username: userManager.USERNAME,
                session_name: userManager.SESSION,
                session_ver: userManager.SESSION_VER,
                block_iden: unitManager.SELECTED.data().req.block_iden,
                project_name: unitManager.SELECTED.data().req.project_name,
                block_ver: unitManager.SELECTED.data().req.block_ver,
                annotation_num: idx
            }, function (data, status) {
                if (!data.success) return userManager.failAjax(data, status);
                unitManager.getAnnotations(unitManager.SELECTED.data().res.annotation_path);
                unitManager.logger('Delete-Unit-Annotation', {
                    username: userManager.USERNAME,
                    session_name: userManager.SESSION,
                    session_ver: userManager.SESSION_VER,
                    block_iden: unitManager.SELECTED.data().req.block_iden,
                    project_name: unitManager.SELECTED.data().req.project_name,
                    block_ver: unitManager.SELECTED.data().req.block_ver,
                    annotation_num: idx
                });
            });

        }
    })
})(unitManager);