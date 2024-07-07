import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AppRoutes from './AppRoutes';
import { Layout } from './components/Layout';
import Home from './components/Home';
import './custom.css';
import { NavMenu } from './components/NavMenu';
import Player from './components/Player';


const App = () => {
    return (
        <Router>
            <Layout>
                <Routes>
                    <Route path="/" element={<Home />} /> 
                </Routes>
            </Layout>
        </Router>
    );
}

export default App;
