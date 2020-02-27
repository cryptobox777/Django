from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from .models import Post
from .forms import LoginForm, UserCreateForm


User = get_user_model()


class IndexView(generic.ListView):
    model = Post


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'ThreeLineDiary/login.html'


class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'ThreeLineDiary/home.html'


class UserCreate(generic.CreateView):
    """ユーザー登録"""
    template_name = 'ThreeLineDiary/user_create.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = True
        user.save()
        return redirect('ThreeLineDiary:user_create_complete')


class UserCreateComplete(generic.TemplateView):
    """ユーザー本登録"""
    template_name = 'ThreeLineDiary/user_create_complete.html'


class OnlyYouMixin(UserPassesTestMixin):
    """本人か、スーパーユーザーだけユーザーページアクセスを許可する"""
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class UserDetail(OnlyYouMixin, generic.DetailView):
    """ユーザーの詳細ページ"""
    model = User
    template_name = 'ThreeLineDiary/user_detail.html'  # デフォルトユーザーを使う場合に備え、きちんとtemplate名を書く



