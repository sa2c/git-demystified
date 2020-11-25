montage img/0-working-directory.png \
        img/1-add-red.png \
        img/1-empty-commit.png \
        -tile 3x1 \
        -geometry +0+0 \
        img/trees1.png

montage img/0-working-directory.png \
        img/2-add_green.png \
        img/1-empty-commit.png \
        -tile 3x1 \
        -geometry +0+0 \
        img/trees2.png

montage img/0-working-directory.png \
        img/2-add_green.png \
        img/3-commit_red_and_green.png \
        -tile 3x1 \
        -geometry +0+0 \
        img/trees3.png

montage img/5-edit_original.png \
        img/2-add_green.png \
        img/3-commit_red_and_green.png \
        -tile 3x1 \
        -geometry +0+0 \
        img/trees4.png

montage img/5-edit_original.png \
        img/7-stage_colors_green.png \
        img/3-commit_red_and_green.png \
        -tile 3x1 \
        -geometry +0+0 \
        img/trees5.png
