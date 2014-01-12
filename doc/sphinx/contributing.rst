Tham gia phát triển
===================

Mã nguồn ibus-bogo được đặt trên `Github`.

Để tham gia viết code bạn cần biết cách sử dụng `git`_ và lập trình bằng
`python`_.

Hãy fork và tạo một branch mới từ branch ``develop`` (xem phần Git Flow
bên dưới), sau đó viết code và gửi chúng tôi một `pull request`_. Chúng
tôi sẽ xem xét và commit code của bạn trong thời gian sớm nhất.

Tuy nhiên, bạn cũng có thể đóng góp theo những cách đơn giản hơn như
sử dụng phiên bản unstable và thông báo lỗi, viết hướng dẫn sử dụng,
viết blog, chia sẻ với bạn bè và người thân về bộ gõ tiếng Việt này.

Mọi sự đóng góp của các bạn dù dưới hình thức nào cũng đều được chúng tôi
hết sức trân trọng.

.. _Github: https://github.com/BoGoEngine/ibus-bogo-python
.. _git: http://git-scm.com/book
.. _python: http://www.greenteapress.com/thinkpython/
.. _pull request: https://help.github.com/articles/using-pull-requests

Cấu trúc code
-------------

Chúng tôi cố gắng module hóa phần mềm để dễ dàng chuyển sang các nền tảng
khác nên BoGo được chia làm 2 thành phần là IBus engine và BoGo engine.
BoGo engine là phần xử lý tiếng Việt chính nằm trong thư mục ``/bogo``
có API đơn giản (hàm ``process_key()``). Còn IBus engine là phần giao tiếp
với IBus, gồm tất cả các file và thư mục con trong ``/engine`` có nhiệm vụ
gọi hàm `process_key`, đưa kết quả cho người dùng và tạo giao diện tinh
chỉnh phương pháp gõ.

Documentation
-------------

Chúng tôi cũng cố gắng viết code thật dễ hiểu với documentation,
comment đầy đủ trong code nên hi vọng bạn sẽ không cảm thấy khó khăn
khi tìm hiểu BoGo.

Thành phần IBus engine có sử dụng các thư viện ngoài của IBus, Gtk và GLib/GIO.
Bạn có thể tìm thấy tài liệu về cách sử dụng chúng dưới đây:

* IBus: http://ibus.googlecode.com/svn/docs/ibus-1.5/index.html
* Gtk: http://python-gtk-3-tutorial.readthedocs.org/en/latest/index.html
* GIO: http://developer.gnome.org/gio/unstable/

Testing
-------

Nhóm phát triển ibus-bogo sử dụng phương pháp TDD (test-driven
development) để phát triển phần mềm. Khi đóng góp cho BoGo, bạn luôn phải
viết test mỗi khi thay đổi code. Các test case có thể tìm thấy trong thư
mục ``/test``.

Git Flow
--------

ibus-bogo được quản lý bằng Git.  Phương pháp này sử dụng có thể trình
bày sơ lược như sau:

- Repo chính trên Github luôn có 2 branch là ``master`` và ``develop``. ``master``
  luôn chứa phiên bản stable mới nhất còn ``develop`` là branch chứa tất cả
  những thay đổi mới nhất của BoGo. Tuy nhiên, thường ít khi commit trực tiếp
  vào ``develop`` ngoài những commit sửa lỗi nhỏ.

- Khi thực hiện một tính năng mới thì lập trình viên tạo branch mới với
  tên ``feature/<tên tính năng>``. Khi đã cảm thấy đủ chín thì merge branch
  này với ``develop`` và xóa branch ``feature/*`` đi. Từ sau trở đi tính năng
  này sẽ được maintain trong branch ``develop``.

- Khi có đủ tính năng mới và các lỗi quan trọng đã được sửa thì có thể
  tính đến việc release phiên bản major mới. Khi đó tạo branch ``release/v<phiên bản>``
  và thực hiện tất cả các commit sửa lỗi cho phiên bản này tại đây. Khi tất
  cả các lỗi trước khi phát hành được sửa hết thì sửa version string trong
  source code, tạo tag cho phiên bản mới và merge vào master. Trong toàn
  bộ quá trình này, các thay đổi mới vẫn thực hiện ở các feature branch
  và ``develop`` như bình thường. Sau khi release thì các commit ở ``release/*``
  được merge trở lại vào ``develop``.

- Sau khi release phiên bản major mà phát hiện lỗi đặc biệt nghiêm trọng
  nào đó thì phải sửa ngay lập tức và release phiên bản minor với branch
  ``hotfix/v<phiên bản>``. Quy trình giống như một branch ``release/*``.
  Sau khi release phải merge lại vào ``develop``.

Chi tiết về phương pháp git flow:
    http://nvie.com/posts/a-successful-git-branching-model/

Công cụ hỗ trợ ``git-flow``:
    http://jeffkreeftmeijer.com/2010/why-arent-you-using-git-flow/
