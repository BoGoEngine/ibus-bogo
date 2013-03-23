## Build gói debian

Cần cài gói:

* devscripts

Commands:

    $ git checkout debian
    $ git checkout -b build
    $ git merge master
    $ debuild -us -uc
   
(optional - xóa branch build)

    $ git branch -D build

**Ghi chú:** debian là một branch riêng chỉ chứa thư mục debian. Do vậy nên
không được merge trực tiếp vào đây mà phải copy sang branch build mới được merge.
