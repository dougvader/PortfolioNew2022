import Home from './components/Home.js';
import { Route } from 'react-router-dom';
import Layout from './components/Layout.js';

const AppRoutes = () => {
    return (
        <div>
            {/* Parent Route */}
            <Route path="/" element={<Layout>
                <Route index element={<Home />} />
            </Layout>} />
        </div>
    );
};

export default AppRoutes;
