# Django Project

## Langkah untuk Menjalankan di Lokal

### 1. Membuat Database Gambar di Lokal (PostgreSQL)

Jalankan perintah berikut untuk memulai layanan Docker yang akan membuat dan mengkonfigurasi database PostgreSQL:

```sh
docker-compose up
```

### 2. Menjalankan Tailwind CSS

Jalankan perintah berikut untuk memulai proses pengembangan Tailwind CSS:

```sh
python manage.py tailwind start
```

### 3. Menjalankan Server Web Django

Jalankan perintah berikut untuk memulai server pengembangan Django:

```sh
python manage.py runserver
```

### 4. Menjalankan Celery

```sh

cd .\env\Scripts\
.\activate
cd ..\..

celery -A coldemail worker --pool=solo -l info # untuk running worker

celery -A coldemail beat -l info # untuk logging check celery

```

---

## Registrasi Akun Staf pada Algo Network

#### Deskripsi Singkat

Bagian ini menjelaskan proses registrasi akun tipe staf pada aplikasi Algo Network. Hanya pengguna dengan peran superuser yang memiliki akses untuk membuat akun staf. Akun staf memungkinkan pengguna untuk masuk ke dalam web Algo Network.

#### Penjelasan Registrasi Akun Staf

1. **Akses Halaman Registrasi**:

   - Superuser akses ke halaman registrasi (buat akun staf) di web Algo Network.
   - Halaman registrasi hanya dapat diakses oleh pengguna yang telah login dengan akun superuser.

2. **Akses Akun Staf**:
   - Setelah registrasi berhasil, pengguna dapat menggunakan akun staf untuk masuk ke dalam web Algo Network.
   - Pengguna dapat mengakses fitur dan fungsionalitas tertentu yang tersedia dalam aplikasi.

---

## Standar Commit

Dengan format di atas, instruksi akan lebih mudah dipahami dan diikuti, serta standar commit akan membantu menjaga konsistensi dan kualitas riwayat commit dalam proyek ini.

## Commit Standard

source : https://www.freecodecamp.org/news/how-to-write-better-git-commit-messages/

Conventional Commits
Now that we've covered basic commit structure of a good commit message, I'd like to introduce Conventional Commits to help provide some detail on creating solid commit messages.

At D2iQ, we use Conventional Commit which is a great practice among engineering teams. Conventional Commit is a formatting convention that provides a set of rules to formulate a consistent commit message structure like so:

```
    <type>[optional scope]: <description>

    [optional body]

    [optional footer(s)]

```

The commit type can include the following:

- `feat`: Introduces a new feature with the changes.
- `fix`: Indicates a bug fix has occurred.
- `chore`: Covers changes that are unrelated to a fix or feature and don't modify src or test files, such as updating dependencies.
- `refactor`: Refactors code without fixing a bug or adding a feature.
- `docs`: Updates to documentation such as the README or other markdown files.
- `style`: Changes that do not affect the meaning of the code, often related to code formatting like white-space or missing semi-colons.
- `test`: Includes new or corrected tests.
- `perf`: Indicates performance improvements.
- `ci`: Related to continuous integration.
- `build`: Changes that affect the build system or external dependencies.
- `revert`: Reverts a previous commit.

The commit type subject line should be all lowercase with a character limit to encourage succinct descriptions.

The optional commit body should be used to provide further detail that cannot fit within the character limitations of the subject line description.

It is also a good location to utilize BREAKING CHANGE: `<description>` to note the reason for a breaking change within the commit.

The footer is also optional. We use the footer to link the JIRA story that would be closed with these changes for example: `Closes D2IQ-<JIRA #>`.

Full Conventional Commit Example

```
    fix: fix foo to enable bar

    This fixes the broken behavior of the component by doing xyz.

    BREAKING CHANGE
    Before this fix foo wasn't enabled at all, behavior changes from <old> to <new>

    Closes D2IQ-12345
```

### Commit Message Comparisons

Review the following messages and see how many of the suggested guidelines they check off in each category.

**Good:**

1. `feat: improve performance with lazy load implementation for images`
2. `chore: update npm dependency to latest version`
3. `Fix bug preventing users from submitting the subscribe form`
4. `Update incorrect client phone number within footer body per client request`

**Bad:**

1. `fixed bug on landing page`
2. `Changed style`
3. `oops`
4. `I think I fixed it this time?`
5. _empty commit messages_

Writing good commit messages is an extremely beneficial skill to develop, and it helps you communicate and collaborate with your team. Commits serve as an archive of changes. They can become an ancient manuscript to help us decipher the past, and make reasoned decisions in the future.

# Deskripsi Fitur

## Generator Email (FE + BE)

Pastikan telah melakukan migrasi terlebih dahulu:
python manage.py makemigrations
python manage.py migrate
Fitur ini memungkinkan user untuk memasukkan inputan prompt untuk membuat email.
