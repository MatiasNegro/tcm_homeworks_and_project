import 'package:flutter_app/pages/startGrid.dart';
import 'package:flutter/material.dart';
import 'pages/classes.dart';
import 'pages/home.dart';
import 'pages/results.dart';

void main() {
  runApp(MaterialApp(
    initialRoute: '/',
    routes: {
      '/': (context) => Home(),
      '/classes': (context) => Class(),
      '/reuslts': (context) => Results(),
      '/startGrid': (context) => StartGrid()
    },
  ));
}
