# BoGo Input Method Engine for IBus


## Introduction

**IBusBoGoEngine** là một engine xử lý gõ tiếng Việt cho IBus, một chương trình xử lý nhập dữ liệu từ bàn phím phổ biến trong GNU/Linux. **IBusBoGoEngine** được viết bằng ngôn ngữ Python và xử dụng engine xử lý tiếng Việt **BoGoEngine**.

Mailing list của nhóm phát triển: bogoengine-dev@googlegroups.com

## Tài liệu

Tài liệu của dự án sẽ được cung cấp trong thời gian sớm nhất. Mọi trợ giúp về sử dụng và phát triển liên hệ mailing list của nhóm phát triển:

## Yêu cầu

### Cho việc biên dịch

* python 2.7
* glibmm 2.4
* gcc 4.2+
* CMake 2.6+

### Cho việc sử dụng

* glibmm 2.4
* gcc 4.2
* ibus 1.4

## Hướng dẫn build

### Build bình thường

Cài đặt:

    $ mkdir build && cd build
    $ cmake .. && make install

Gỡ cài đặt:
    $ cd build && sudo make uninstall

### Build gói debian

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

## Giấy phép xuất bản (License)

Toàn bộ mã nguồn của **IBusBoGoEngine** và **BoGoEngine** cùng tất cả các tài nguyên đi kèm đều được phát hành dưới các quy định ghi trong Giấy phép Công cộng GNU, phiên bản 3.0 (GNU General Public License v3.0).  Xem tệp *COPYING* để biết thêm chi tiết.

## Cretdit

Bản quyền (C) năm 2012 bởi:

* Đàm Tiến Long <longdt90@gmail.com>
* Trung Ngo <ndtrung4419@gmail.com>

