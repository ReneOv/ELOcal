import { RouteProps } from "react-router-dom";

export type ProtectedRouteProps = RouteProps & {
    outlet: JSX.Element;
};

export function ProtectedRoute({ outlet }: ProtectedRouteProps) {
    return outlet;
}