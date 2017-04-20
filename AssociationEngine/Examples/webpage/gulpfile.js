var babelify = require('babelify');
var browserify = require("browserify");
var browserSync = require('browser-sync').create();
var buffer = require('vinyl-buffer');
var concat = require('gulp-concat');
var gulp = require('gulp');
var gutil = require('gulp-util');
var jetpack = require('fs-jetpack');
var ngAnnotate = require('browserify-ngannotate');
var notify = require("gulp-notify");
var sass = require('gulp-sass');
var source = require("vinyl-source-stream");
var sourcemaps = require('gulp-sourcemaps');
var streamify = require("gulp-streamify");
var uglify = require("gulp-uglify");
var watchify = require('watchify');

var srcDir = jetpack.cwd('src');
var distDir = jetpack.cwd('dist');

gulp.task('build', ['copy', 'concat-css'], function() {
    return buildScript('main.js', false);
});

function handleErrors() {
    var args = Array.prototype.slice.call(arguments);
    notify.onError({
        title: "Compile Error",
        message: "<%= error.message %>"
    }).apply(this, args);
    this.emit('end'); // Keep gulp from hanging on this task
}

/*
 * Watches files and updates the build on change
 * 
 * Based on: http://blog.avisi.nl/2014/04/25/how-to-keep-a-fast-build-with-browserify-and-reactjs/
 */
function buildScript(file, watch) {

    var props = { entries: [srcDir.path() + '/' + file], debug: true, cache: {}, packageCache: {} };
    var bundler = watch ? watchify(browserify(props)) : browserify(props);
    bundler.transform('babelify', { 'presets': ['es2015'] });
    bundler.transform(ngAnnotate);

    function rebundle() {
        var stream = bundler.bundle();

        if (watch) {
            return stream.on('error', handleErrors)
                .pipe(source(file))
                .pipe(buffer())
                .pipe(sourcemaps.init({ loadMaps: true }))
                .pipe(sourcemaps.write('./'))
                .pipe(gulp.dest(distDir.path() + '/'));
        } else {
            return stream.on('error', handleErrors)
                .pipe(source(file))
                .pipe(buffer())
                .pipe(sourcemaps.init({ loadMaps: true }))
                .pipe(streamify(uglify().on('error', gutil.log)))
                .pipe(sourcemaps.write('./'))
                .pipe(gulp.dest(distDir.path() + '/'));
        }

    }

    bundler.on('update', function() {
        rebundle();
        gutil.log('Rebundle...');
    });

    return rebundle();
}

gulp.task('copy', ['clean'], function() {

    return srcDir.copy('.', distDir.path(), {
        matching: ['partial/**/*.html', 'index.html', 'svg/**/*.svg', 'img/**/*.png', '*.ico']
    });

});

gulp.task('clean', function() {

    return distDir.remove();

});

gulp.task('watch:js', function() {
    gulp.watch("dist/*.js").on('change', browserSync.reload);

});

gulp.task('watch:html', function() {
    gulp.watch(["src/partial/**/*.html", 'src/index.html']).on('change', function() {

        srcDir.copy('.', distDir.path(), {
            matching: ['partial/**/*.html', 'index.html'],
            overwrite: true
        });

        browserSync.reload();
    });
});

gulp.task('watch:sass', function() {

    gulp.watch('src/styles/**/*.sass', function() {

        distDir.remove('css');

        gulp.src(srcDir.path('styles/**/*.sass'))
            .pipe(sass().on('error', sass.logError))
            .pipe(gulp.dest(distDir.path('css'))).on('end', function() {

                gulp.src([
                        'dist/css/*.css',
                        'node_modules/angular-material/angular-material.min.css'
                    ])
                    .pipe(concat('css/style.css'))
                    .pipe(gulp.dest(distDir.path())).on('end', browserSync.reload);

            });
    });

});

/**
 * Main task for development.
 */
gulp.task('default', ['build', 'watch:js', 'watch:html', 'watch:sass'], function() {

    // Reload all connected browsers proxying our server when changes made to src/
    browserSync.init({
        server: {
            baseDir: "dist/"
        }
    });

    return buildScript('main.js', true);
});

gulp.task('app-css', function() {

    return gulp.src(srcDir.path('styles/**/*.sass'))
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest(distDir.path('css')));

});

gulp.task('vendor-css', function() {

    return gulp.src([
            'node_modules/angular-material/angular-material.min.css'
        ])
        .pipe(gulp.dest(distDir.path('css')))

});

gulp.task('concat-css', ['vendor-css', 'app-css'], function() {

    gulp.src([
            'dist/css/*.css',
        ])
        .pipe(concat('css/style.css'))
        .pipe(gulp.dest(distDir.path()));

});

gulp.task('debug', ['copy', 'concat-css'], function() {

    return browserify('./src/main')
        .transform(ngAnnotate)
        .bundle()
        .pipe(source('main.js'))
        .pipe(gulp.dest('./dist'));

});