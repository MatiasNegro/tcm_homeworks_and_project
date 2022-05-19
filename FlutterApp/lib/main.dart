import 'package:flutter/material.dart';
import 'pages/classes.dart';
import 'pages/home.dart';

void main() {
  runApp(MaterialApp(
    initialRoute: '/',
    routes: {'/': (context) => Home(), '/classes': (context) => Class()},
  ));
}
